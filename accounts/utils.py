def api_response(**kwargs):

    action = kwargs["action"]
    method = kwargs["method"]
    url = kwargs["url"]
    error = kwargs["error"]
    message = kwargs["message"]
    status = kwargs["status"]

    if error!= "":
        res = {
            "action": action,
            "method": method,
            "url": url,
            "error": error,
            "status": status,
        }
        return res
        
    else:
        res = {
            "action": action,
            "method": method,
            "url": url,
            "message": message,
            "status": status,
        }

        return res