import requests
from picamera import PiCamera
from time import sleep

SERVER_URL = 'http://192.168.43.138:3000'
USER_ID = 1
TITLE = 'Home'
PHOTO_FILENAME = 'home_photo'
DELAY = 300
IS_TEMP = True
PREVIEW_DELAY = 4
MODE = 'cycle' # or 'single'

class MyCamera:
    def __init__(self, is_temp, filename, preview_delay):
        self.is_temp = is_temp
        self.counter = 0
        self.filename = filename
        self.preview_delay = preview_delay
        self.camera = PiCamera()
    
    def capture(self):
        self.camera.start_preview()
        sleep(self.preview_delay)
        self.camera.capture(self.filename + str(self.counter) + '.jpg')
        self.camera.stop_preview()
        if not self.is_temp:
            self.counter += 1
        return self.filename


class PostRequest: 
    def __init__(self, url, user_id, title):
        self.url = url
        self.params = (('image[user_id]', str(user_id)),('image[title]', str(title)))
        
    def make_request(self, filename):
        self.files = ('image[photo]', open(filename, 'rb'))
        requests.post(self.url, files = self.files, data = self.params)
        self.files['image[photo]'].close()

class Client:
    TEMP_FILENAME = 'temp_photo'
    def __init__(self, server_url, photo_filename=TEMP_FILENAME, delay=0, preview_delay=2, is_temp=True, user_id=1, title='Title'):
        self.server_url = server_url
        self.photo_filename = photo_filename
        self.delay = delay
        self.preview_delay = preview_delay
        self.is_temp = is_temp
        self.user_id = user_id
        self.title = title
        self.my_camera = MyCamera(self.is_temp, self.photo_filename, self.preview_delay)
        self.post_request = PostRequest(self.server_url, self.user_id, self.title)
    
    def single_capture_and_post(self):
        filename = self.my_camera.capture()
        self.post_request.make_request(filename)
    
    def cycle_capture_and_post(self):
        while True:
            filename = self.my_camera.capture()
            self.post_request.make_request(filename)
            sleep(self.delay)

if __name__ == '__main__':
    client = Client(SERVER_URL, PHOTO_FILENAME, DELAY, PREVIEW_DELAY, IS_TEMP, USER_ID, TITLE)
    if MODE == 'single':
        client.single_capture_and_post()
    elif  MODE == 'cycle':
        client.cycle_capture_and_post()