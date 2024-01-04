from hugchat import hugchat
from hugchat.login import Login
# Log in to huggingface and grant authorization to huggingchat
email='fernandezmiguezmanuel@gmail.com'
passwd='Soymuyguapo1'
sign = Login(email, passwd)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

# Load cookies when you restart your program:
# sign = login(email, None)
# cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

# non stream response
def funcionchat(id,superid):
    #sign = Login(email, None)
    cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
    query_result = chatbot.query(f"Please, classify the entity '{id}'  into one of the agrovoc narrowers of the superior concept {superid} or that concept, you must to retrieve only the name of the subconcept without further words",web_search=False)
    parts = str(query_result).split("*")
    if(len(parts)>1):
        return parts[1] # or query_result.text or query_result["text"]
    else:
        return parts[0]
print(funcionchat("laboratory animals housing","http://aims.fao.org/aos/agrovoc/c_3678"))