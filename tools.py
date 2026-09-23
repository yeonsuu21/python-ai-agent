import csv
import sqlite3
from datetime import datetime


SCHEDULE_FILE = "data/schedule.csv"
EMPLOYEE_DB = "data/employee.db"


# 1. 공연 일정 조회
def get_schedule(start_date, end_date):
    schedules = []

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    with open(SCHEDULE_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            schedule_date = datetime.strptime(row["date"], "%Y-%m-%d")

            if start <= schedule_date <= end:
                schedules.append(row)

    return schedules


# 2. 담당자 정보 조회
def get_employee(name):
    connection = sqlite3.connect(EMPLOYEE_DB)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name, email
        FROM employees
        WHERE name = ?
        """,
        (name,)
    )

    employee = cursor.fetchone()

    connection.close()

    if employee is None:
        return {
            "error": f"{name} 담당자를 찾을 수 없습니다."
        }

    return {
        "name": employee[0],
        "email": employee[1]
    }


# 3. 담당자 업무량 계산
def calculate_workload(employee):
    count = 0

    with open(SCHEDULE_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["manager"] == employee:
                count += 1

    return {
        "employee": employee,
        "schedule_count": count
    }


# 4. 이메일 초안 생성
def create_email_draft(employee, schedules):

    schedule_text = ""

    for schedule in schedules:
        schedule_text += (
            f"- {schedule['date']} "
            f"{schedule['performance']}\n"
        )

    subject = "공연 일정 안내"

    body = f"""안녕하세요, {employee}님.

담당 공연 일정을 안내드립니다.

{schedule_text}

확인 부탁드립니다.
감사합니다.
"""

    return {
        "employee": employee,
        "subject": subject,
        "body": body
    }