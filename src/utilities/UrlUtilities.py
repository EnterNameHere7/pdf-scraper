
class UrlUtilities:

    def fix_url(previous_url: str, url: str, domain: str):
        if domain not in url:
            # this means it's trying to use relative paths lets fix them

            if url.startswith("../"):
                if previous_url.endswith("/"):
                    previous_url = previous_url[:-1]

                url = previous_url[:previous_url.rfind('/')] + "/" + url.replace("../", "")
            elif url.startswith("/"):
                url = domain + url
            elif url.startswith("#"):
                raise ValueError("Url can't start with a #")
            elif "/" not in url:
                if ".html" in previous_url:
                    url = previous_url[:previous_url.rfind('/')] + "/" + url
                else:
                    url = previous_url.rstrip("/") + "/" + url
            else:
                if not url.startswith("http"):
                    if ".html" in previous_url:
                        url = previous_url[:previous_url.rfind('/')] + "/" + url
                    else:
                        url = previous_url.rstrip("/") + "/" + url
                else:
                    url = previous_url + url
        return url