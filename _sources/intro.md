# HeatHack Data Book

This website shows plots of temperature and relative humidity data for HeatHack's participating venues and allows you to download the data for plotting yourself.  To use it, you'll need your venue number.  We don't use venue names, for security.

For those with internet-connected monitors that rely on the building's wifi, the data will be transferred here automatically every few hours.  If you need to see whether you have data coming in faster than that and you have an internet-connected sensor, you can look at your recent data on ThingSpeak, but there is still an arbitrary time delay before it will appear.

- [ThingSpeak data plots](https://uk.mathworks.com/matlabcentral/profile/authors/15201195?detail=thingspeak)

For those with standalone monitors, we currently have to hand-process the data, so there may be more of a lag before you see it.  Your data will not be available on ThingSpeak, but appear directly here.  The sensor units don't contain a proper clock, so the times will progressively get further "out" the longer you leave it without downloading the data.  We may be able to correct the times when we process the data, but for now we just let them be a bit out.  

```{tableofcontents}
```