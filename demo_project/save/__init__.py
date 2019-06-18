import logging
import requests
import json
import azure.functions as func


def send_simple_message(data, email):
    to_address = ["Saman A. Pour <samanemail>"]
    if len(email) > 1:
        to_address.append(email)
    return requests.post(
        "https://api.mailgun.net/v3/mail.samanamp.com/messages",
        auth=("api", "45632a0e0777363219e2d3ab3bdf304c-16ffd509-4a490589"),
        data={"from": "Saman A. Pour <samanemail>",
              "to": to_address,
              "subject": "Feedback Form",
              "html": data})


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    formdata = json.loads(req.get_body().decode('utf-8'))

    experience_level = {
        "Select ...": "Not selected",
        "1": "< 1 year",
        "2": "1 - 5 years",
        "3": "5 - 10 years",
        "4": "10+ years"
    }
    content_applicable_for = "" + (" My current job." if formdata['content_for_current_job'] else "") + (
        " A job I would like to pursue." if formdata['content_for_pursue'] else "") + (
                                 " A side project I’m working on." if formdata['content_for_side_project'] else "") + (
                                 " My general interests." if formdata['content_for_interest'] else "")
    print(content_applicable_for)
    data = f"""<html>
    <h1>Feedback Form</h1>
    <p><b>Jobtitle: </b><br/> {formdata['attendee_job_title']}</p>
    <p><b>For how many years have you been employed as a developer (if applicable)?: </b><br/> {experience_level[
        formdata['attendee_experience_level']]}</p>
    <p><b>The content was applicable to (select as many as applicable)... </b><br/> {content_applicable_for}</p>
    <p><b>The difficulty level and pace of the Lunch & Learn was appropriate: </b><br/> {formdata[
        'content_difficulty_level']}</p>
    <p><b>The Lunch & Learn was interesting and sparked my curiosity on the subject matter: </b><br/> {formdata[
        'content_interesting_level']}</p>
    <p><b>How would you rate the instructor’s level of expertise on the subject matter? </b><br/> {formdata[
        'instructor_knowledge']}</p>
    <p><b>Any additional feedback/comments for the instructor? </b><br/> {formdata['instructor_feedback']}</p>
    <p><b>What was the most valuable part of the Lunch&Learn? Least valuable? </b><br/> {formdata[
        'valuable_part_feedback']}</p>
    <p><b>What topic(s) would you like to hear (more) about in the future? </b><br/> {formdata[
        'topics_of_interest_feedback']}</p>
    <p><b>Attendee's Email: </b><br/> {formdata['attendee_email']}</p>
    </html>"""

    send_simple_message(data, formdata['attendee_email'])

    return func.HttpResponse(json.dumps({"result": "succeeded"}), mimetype="application/json")
