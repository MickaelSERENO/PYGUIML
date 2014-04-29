#!/usr/bin/python

import time
from PIL import Image
from gi.repository import GObject
from gi.repository import Gst
import sfml as sf
import io
from Widget import Widget

GObject.threads_init()
Gst.init(None)

class VideoManager(Widget):
    def __init__(self, parent=0, path=None, rect=sf.Rectangle()):

        self._texture = sf.Texture.create(1,1)
        self._sprite = sf.Sprite(self._texture)
        self.path = path

        #The player
        self.player = Gst.ElementFactory.make("playbin", "player")

        #Config the video output
        binVideo = Gst.Bin()
        videoScale = Gst.ElementFactory.make("videoscale", "videoScale")
        videoScale.set_property("method", 0)
        self.videoFilter = Gst.ElementFactory.make("capsfilter", "videoFiltered")
        videoConvert = Gst.ElementFactory.make("videoconvert", "videoConvert")
        self.videoSink=Gst.ElementFactory.make("appsink", "videoSink")
        self.videoSink.set_property("max_buffers", 8)
        self.videoSink.set_property("drop", True)
        self.videoSink.set_property("sync", True)
        self.videoSink.set_property("async", False)
        self.videoSink.set_property("emit-signals", True)
        self.videoSink.connect("new-preroll", self.initTexture)

        videoCaps = Gst.Caps("video/x-raw, format=(string)RGBx")
        self.videoFilter.set_property("caps", videoCaps)
        self.videoCaps = Gst.Caps(videoCaps.to_string())

        #Add and link the elements to the bin video
        binVideo.add(videoScale)
        binVideo.add(self.videoFilter)
        binVideo.add(videoConvert)
        binVideo.add(self.videoSink)
        videoScale.link(self.videoFilter)
        self.videoFilter.link(videoConvert)
        videoConvert.link(self.videoSink)
        pad = videoScale.get_static_pad("sink")
        ghostPad = Gst.GhostPad.new("sink", pad)
        binVideo.add_pad(ghostPad)

        self.player.set_property("video-sink", binVideo)

        if path:
            self.player.set_property("uri", Gst.filename_to_uri(path))
        self.player.set_state(Gst.State.PLAYING)

        Widget.__init__(self, parent, rect)
        self.pos = rect.position
        self.size = rect.size

        self._speed = 1
        self.requestTime = 10**9*60
        self._canSetSpeed = False

        self.bus = self.player.get_bus()
        self.streamStart = False

    def __del__(self):
        self.player.set_state(Gst.State.NULL)

    def update(self, render=None):
        videoSample = self.videoSink.get_property("last-sample")
        if videoSample:
            videoBuf = videoSample.get_buffer()
            videoData = videoBuf.extract_dup(0, videoBuf.get_size())

            pixels = sf.Pixels()
            pixels.data = videoData
            pixels.width = self._texture.width
            pixels.height = self._texture.height
            self._texture.update_from_pixels(pixels)

        message = self.bus.pop()
        while message:
            if message.type == Gst.MessageType.STREAM_START:
                self.initVideo()
            message = self.bus.pop()

        Widget.update(self, render)

    def draw(self, render=None):
        if render:
            render.draw(self._sprite)

    def setSize(self, size, resetOrigin=True):
        if size == sf.Vector2(0,0):
            return

        Widget.setSize(self, size, resetOrigin)
        self._texture = sf.Texture.create(self.size.x, self.size.y)
        self._sprite = sf.Sprite(self._texture)
        self.videoCaps.set_value("width", self.size.x)
        self.videoCaps.set_value("height", self.size.y)

        self.videoFilter.set_property("caps", Gst.Caps(self.videoCaps.to_string()))

    def setPos(self, pos, withOrigin=True):
        Widget.setPos(self, pos, withOrigin)
        self._sprite.position = self.pos

    def initTexture(self, appsink):
        videoSample = self.videoSink.get_property("last-sample")
        videoCap = videoSample.get_caps()
        videoStruct = videoCap.get_structure(0)

        self._texture = sf.Texture.create(videoStruct.get_value("width"), videoStruct.get_value("height"))
        self._sprite = sf.Sprite(self._texture)

        return Gst.FlowReturn.OK

    def initVideo(self):
        self.streamStart = True
        self.setSpeed(self._speed)
        if self.requestTime:
            self.setCurrentTimeInNs(self.requestTime)
            self.requestTime = None

    def setSpeed(self, speed):
        if not self.streamStart:
            return
        self._speed = speed

        seekFlags = Gst.SeekFlags.SKIP | Gst.SeekFlags.ACCURATE | Gst.SeekFlags.FLUSH
        seekEvent = Gst.Event.new_seek(self._speed, Gst.Format.TIME,\
                seekFlags, Gst.SeekType.SET, self.time, \
                Gst.SeekType.NONE, 0)
        self.player.send_event(seekEvent)

    def getCurrentTimeInNs(self):
        return self.player.query_position(Gst.Format.TIME)[1]
    
    def setCurrentTimeInNs(self, time):
        if not self.streamStart:
            self.requestTime = time
            return
        self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.SKIP | Gst.SeekFlags.ACCURATE | Gst.SeekFlags.FLUSH, time)

    def getDurationInNs(self):
        return self.player.query_duration(Gst.Format.TIME)[1]

    def setVolume(self, volume):
        self.player.set_property("volume", volume)

    def getVolume(self):
        return self.player.get_property("volume")

    time = property(getCurrentTimeInNs, setCurrentTimeInNs)
    speed = property(lambda self:self._speed, setSpeed)
    volume = property(getVolume, setVolume)
