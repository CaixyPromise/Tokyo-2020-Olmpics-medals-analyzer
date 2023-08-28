import time
from PIL import Image, ImageTk, ImageSequence
import cv2
__all__ = ['MediaViewer']

class AnimatedGifPlayer:
    def __init__(self, label, delay=0.04):
        self.label = label
        self.delay = delay
        self.stop = False
        self._num = 0
        self.after_id = None

    def play_animation(self, gif_file, size=None):
        self.gif_file = gif_file
        self.size = size
        self.start_time = time.time()
        self.stop = False
        self._animate()

    def stop_animation(self):
        self.stop = True
        if self.after_id:
            self.label.after_cancel(self.after_id)
        self.label.config(image='')

    def _animate(self):
        try:
            img = Image.open(self.gif_file)
            img.seek(self._num)
            if self.size is not None:
                img = img.resize(self.size, Image.ANTIALIAS)
            self.gif = ImageTk.PhotoImage(img)
            self.label.config(image=self.gif)
            self._num += 1
        except EOFError:
            self._num = 0
        if not self.stop:
            self.after_id = self.label.after(int(self.delay * 1000), self._animate)

class ImageViewer:
    def __init__(self, component, image_path = None, size = None):
        self.component = component
        if (image_path is not None):
            self.show_image(image_path, size)

    def show_image(self, image_path, size = None):
        try:
            image = Image.open(image_path)
            if (size is not None):
                image = image.resize(size)
            photo = ImageTk.PhotoImage(image)
            self.component.config(image = photo)
            self.component.image = photo
        except:
            pass

    def show_cv_image(self, cv_image):
        image = Image.fromarray(cv_image)
        photo = ImageTk.PhotoImage(image)
        self.component.config(image = photo)
        self.component.image = photo

    def show_animated_image(self, image_path, size=None):
        self.frames = []
        self.load_frames(image_path, size)
        self.animate()

    def load_frames(self, gif_path, size):
        im = Image.open(gif_path)
        if (size is not None):
            im = im.resize(size)
        iters = ImageSequence.Iterator(im)
        for frame in iters:
            self.frames.append(ImageTk.PhotoImage(frame))

    def animate(self):
        while True:
            for frame in self.frames:
                self.component.config(image=frame)
                self.component.image = frame
                time.sleep(0.1)
                self.component.update_idletasks()
                self.component.update()


class VideoViewer(ImageViewer):
    def __init__(self, component, video_path = None, size = None):
        super().__init__(component)
        self.size = size
        if video_path is not None:
            self.show_video(video_path, size)
        self.stop = False

    def show_video(self, video_path, size = None):
        if size is not None:
            self.size = size
        self.cap = cv2.VideoCapture(video_path)
        self._update_video()

    def _update_video(self):
        if (not self.stop):
            ret, frame = self.cap.read()
            if ret:
                if self.size is not None:
                    frame = cv2.resize(frame, self.size)
                self.show_cv_image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                self.component.after(10, self._update_video)
            else:
                self.cap.release()

    def stop_video(self):
        self.stop = True
        self.cap.release()
        self.component.config(image = '')



class MediaViewer:
    def __init__(self, component):
        self.component = component
        self.image_viewer = ImageViewer(self.component)
        self.video_viewer = VideoViewer(self.component)
        self.gif_viewer = AnimatedGifPlayer(self.component)
        self.__run = 0

    def show_image(self, image_path, size=None):
        self.image_viewer.show_image(image_path, size)

    def show_cv_image(self, cv_image):
        self.image_viewer.show_cv_image(cv_image)

    def show_video(self, video_path, size=None):
        self.__run = 1
        self.video_viewer.show_video(video_path, size)

    def show_animated_image(self, image_path, size = None):
        self.__run = 2
        self.gif_viewer.play_animation(image_path, size)

    def set_clean(self):
        self.component.config(image = '')
        if (self.__run == 1):

            self.video_viewer.stop_video()
        elif (self.__run == 2):

            self.gif_viewer.stop_animation()
