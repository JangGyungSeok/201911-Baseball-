from decouple import config
#webhook 설정을 위한 경로
url=f'https://api.telegram.org/bot{token}/setWebhook'
#내가 연결하려는 주소
ngrok_url='https://b8f4160d.ngrok.io/telegram'
#실행 주소
setwebhook_url=f"{url}?url={ngrok_url}"
print(setwebhook_url)