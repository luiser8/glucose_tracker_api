import math
import os
from middleware.responseHttpUtils import responseHttpUtils
from middleware.dateTimeUtils import dateTimeUtils
from services.usersMeasurementsSrv import usersMeasurementsSrv

class hba1cSrv():
    def __init__(self):
        self.ADA_HBA1C_INTERCEPT = float(os.getenv("ADA_HBA1C_INTERCEPT"))
        self.ADA_HBA1C_SLOPE =  float(os.getenv("ADA_HBA1C_SLOPE"))
        self.RCI = int(os.getenv("RCI"))
        self.FSI = int(os.getenv("FSI"))
        self.MIN_GLUCOSE_CAL = int(os.getenv("MIN_GLUCOSE_CAL"))
        self.MAX_GLUCOSE_CAL = int(os.getenv("MAX_GLUCOSE_CAL"))
        self.users_measurements = usersMeasurementsSrv()

    def getByUserHba1cSrv(self, user_id, start_date, end_date):
        date_utils = dateTimeUtils().getCalculateDates()
        start_date = start_date if start_date is not None else date_utils["date_3_months_ago"]
        end_date = end_date if end_date is not None else date_utils["current_date"]

        result = self.users_measurements.getByDateRangeSrv(user_id, start_date, end_date)
        if not result or "data" not in result or not result["data"]:
            return responseHttpUtils().response("Error listing measurements", 400, result)

        values = [item['value'] for item in result["data"] if 'value' in item]
        avg_glucose = sum(values) / len(values)
        hba1c = (avg_glucose + self.ADA_HBA1C_INTERCEPT) / self.ADA_HBA1C_SLOPE
        response = round(hba1c, 2)

        return responseHttpUtils().response("HBA1c calculated successfully", 200, {"hba1c": response})

    def calculate_dosis(self, user_id, payload):
        if payload:
            data = {
                'user_id': user_id,
                "actual_glucose": payload["actual_glucose"],
                "objective_glucose": payload["objective_glucose"],
                "carbohydrates": payload["carbohydrates"],
                "rci": self.RCI,
                "fsi": self.FSI
            }

            if not all(isinstance(x, (int, float)) and x > 0 for x in data.values()):
                return responseHttpUtils().response("All values must be positive numbers.", 400, data)

            if data["actual_glucose"] < self.MIN_GLUCOSE_CAL:
                return responseHttpUtils().response("Low glucose (hypoglycemia). Treat with 15-20g of fast-acting carbohydrates and REPEAT the measurement in 15 minutes. Do NOT apply insulin until the glucose is above 100 mg/dL. Consult your doctor.", 200, data)

            if self.MIN_GLUCOSE_CAL <= data["actual_glucose"] < self.MAX_GLUCOSE_CAL:
                return responseHttpUtils().response(f"Slightly low glucose ({data['actual_glucose']} mg/dL). Caution is advised when calculating the dose. It may be necessary to reduce or even omit the correction dose. Consult your doctor.", 200, data)

            if data["objective_glucose"] > data["actual_glucose"]:
                return responseHttpUtils().response("The target glucose cannot be greater than the current glucose. This usually should not happen, as the dose is calculated BEFORE eating.", 400, data)

            insulin_carbohydrates = data["carbohydrates"] / data["rci"]

            glucose_difference = data["actual_glucose"] - data["objective_glucose"]
            if glucose_difference > 0:
                insulin_correction = glucose_difference / data["fsi"]
            else:
                insulin_correction = 0

            total_dose = insulin_carbohydrates + insulin_correction
            result = math.ceil(total_dose)
            if result:
                return responseHttpUtils().response("Calculate dosis successfully", 201, {"dosis": result})
            else:
                return responseHttpUtils().response("Error calculate dosis", 400, result)
