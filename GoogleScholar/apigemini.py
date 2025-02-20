import google.generativeai as genai

genai.configure(api_key="AIzaSyDyPR7lj-MLO6oa86IcSs0kY71pnne4zwU")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("""Return the number of states in usa""")
print(response.text)