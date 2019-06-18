import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    header = """HTTP/1.1 200 OK
            Date: Tue, 11 Jun 2019 00:03:27 GMT
            Expires: -1
            Cache-Control: private, max-age=0
            Content-Type: text/html; charset=ISO-8859-1"""
    with open("./index/index.html") as file:
        return func.HttpResponse(file.read(), mimetype="text/html", status_code=200)

    return func.HttpResponse(
        "Please pass a name on the query string or in the request body",
        status_code=400
    )
