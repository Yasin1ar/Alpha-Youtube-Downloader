#Importing useful and essential libraries
from pytube import YouTube
from pytube import Playlist
from time import sleep
import pytube.request
import getpass
user=str(getpass.getuser())
import os
import ffmpeg

pytube.request.default_range_size = 1048576 # 1MB chunk size

COMPLETED=True
def completed(artist, song_name):
    if COMPLETED==True:
        print(f"\n {status.default_filename} Downloaded successfully\n enjoy :)\n")

def progress_bar(chunk,_fifromle_handle,bytes_remaining):
    print(f"{round(bytes_remaining*0.000001)} MB remaining")

#Getting the link from user, and then diagnosis the link if its the single video URL or a whole playlist
while True:
    link = input('\n Please enter the youtube link : ')
    try:
        ytp=Playlist(link)
        ans=input((f'\n {ytp.title} found! press anything to continue (press "N" or "n" if it\'s not what you want)'))
        if ans not in ('No','no','N','n'):
            break
    except:
        pass
    try:
        yts=YouTube(link,on_progress_callback=progress_bar,on_complete_callback=completed)
        ans=input((f'\n {yts.title} found! press anything to continue (press "N" or "n" if it\'s not what you want)'))
        if ans not in ('No','no','N','n'):
            break
    except:
        print('\n link is not valid, try again')

#Specifying the user desired media format (Video or Audio)
def stat():
    global status
    status = input('\n Audio or video ? (audio=1 \ video=2) ')
    print('Working.....please be patient')
    return status
while stat() not in ('1', '2'):
        print(' --{} Unknown status, please choose 1 or 2 {}--'.format(3*"\N{Cross Mark}",3*"\N{Cross Mark}")) 

#Function for checking the chosen video resolution quality
def vq_available(res):
    global progressive
    global available
    progressive=True
    available = yt.streams.filter(file_extension='mp4').get_by_resolution(res)
    if available:
        return f"{round(available.filesize*0.000001)} MB" 
    else:
        try:
            progressive=False
            available = yt.streams.filter(file_extension='mp4',res=res)
            available = yt.streams.filter(file_extension='mp4',res=res).get_by_itag(available[0].itag)
            global yt_a
            yt_a=yt.streams.filter( adaptive=True , only_audio=True, abr='128kbps').get_audio_only()
            return f"{round(available.filesize*0.000001+yt_a.filesize*0.000001)} MB (adaptive , will merge with ffmpeg)"
        except:
            return 'Unavailable, Resolution does not exist'
#Function for choosing video resolution quality
def video_quality():
    quality = input(f'\n Please choose the resolution ( Note : if you press somthing else, default will be 720p ) \
                    \n 1 -> 1080p {vq_available("1080p")}\n 2 -> 720p {vq_available("720p")} recommended \
                    \n 3 -> 480p {vq_available("480p")}\n 4 -> 360p {vq_available("360p")} \
                    \n 5 -> 240p {vq_available("240p")}\n $ ')

    resolution = {'1':'1080p','2':'720p','3':'480p','4':'360p','5':'240p'}
    res = '720p' 
    if quality == '1': print('Be aware that High quality takes a little time...\n \
    the audio & video must download separately and then they will merge together \ '
    'with ffmpeg and after creating new mp4 file , they will be removed'),sleep(3)
    if quality in resolution.keys() : res = resolution[quality]
    if quality in ('n','N'): quit()
    return res
#If the link is a playlist URL, its not? we ignore this part and move on
try:
    if Playlist(link):
        numoo = 0
        #Only download the audio for all the URL in a Playlist
        if status == '1' :
            print(f'The number of songs are {ytp.length}')
            for url in ytp.videos:
                singer_name=url.author.replace(" - Topic",'')
                path = f'Y:/Music/YD/{singer_name}/{ytp.title}'
                file_name = url.title + '.mp3'
                try:
                    url.streams.get_audio_only().download(output_path = path , filename = file_name)
                    numoo +=1
                except:
                    print(' {} didnt download!'.format(url.title))
                    continue
                print(f'\n {url.title} downloaded successfully {ytp.length}/{numoo}')
        #download the video for all the URL in a Playlist
        elif status == '2':
            print(f'The number of videos are {ytp.length}')
            path = f'P:/Youtube Videos/{ytp.title}'
            for url in ytp.video_urls:
                yt = YouTube(url,on_progress_callback=progress_bar,on_complete_callback=completed)
                print('\n',yt.title)
                status=yt.streams.filter(file_extension='mp4').get_by_resolution('720p')
                try:
                    file_name = status.default_filename 
                    status.download(output_path = path ,filename = file_name)
                    print('\n You getting 720p resolution')
                    numoo +=1
                except AttributeError :
                    status=yt.streams.filter(file_extension='mp4').get_highest_resolution()
                    file_name = status.default_filename
                    status.download(output_path = path ,filename = file_name)
                    print('\n You getting high resolution')
                    numoo +=1
                except:
                    print(' {} didnt download!'.format(status.title))
                print(f'\n {status.title} downloaded successfully {ytp.length}/{numoo}')
        print(f'\n All playlist {ytp.title} downloaded !')
        status = None
except:
    pass
#If the user only want the audio
if status == '1':
    audio = yts.streams.get_audio_only()
    file_name = audio.title+ '.mp3'
    print(f'\t File size -> {round(audio.filesize*0.000001)} MB\n\tFile name -> {file_name}')
    status =  audio
    singer_name=yts.author.replace(" - Topic",'')
    path = f'Y:/Music/YD/{singer_name}'
    status.download(output_path = path ,filename = file_name)

#if the user want the video
elif status == '2':
    yt=yts
    if vq_available(video_quality()):
        if progressive==True:
            print(f'\t File size -> {round(available.filesize*0.000001)} MB\n\tFile name -> {available.default_filename}')
            status = available
            file_name = status.default_filename
            path = 'Y:/Youtube Videos/New folder'
            status.download(output_path = path ,filename = file_name)
            exit()
        else:
            size=available.filesize*0.000001+yt_a.filesize*0.000001
            print(f'\t File size -> {round(size)} MB\n\tFile name -> {available.default_filename}')
            file_name =yt.title+ '.mp3'
            path = 'Y:/Youtube Videos/New folder'
            #Downloading the file that have only audio  
            COMPLETED=False
            try:
                yt_a=yt.streams.filter( adaptive=True , only_audio=True , abr='160kbps' ).get_audio_only()
                status=yt_a
                status.download(output_path=path,filename=file_name) 
            except:
                yt_a=yt.streams.filter( adaptive=True , only_audio=True)
                abr = sorted(list(map(lambda f:f.abr,yt_a)))
                yt_a=yt.streams.filter(adaptive=True,only_audio=True,abr=abr[0]).get_audio_only()
                status=yt_a
                status.download(output_path=path,filename=file_name) 
            #Downloading the file that have only video (no sound) 
            COMPLETED=True
            print('loading......')
            yt_v=available
            status=yt_v
            status.download(output_path = path ,filename = yt_v.default_filename)

    #Merging audio & video into one single mp4 file with the help of ffmpeg
    input_video = ffmpeg.input(f'Y:/Youtube Videos/New folder/{yt_v.default_filename}')
    input_audio = ffmpeg.input(f'Y:/Youtube Videos/New folder/{yt_a.title}.mp3')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'Y:/Youtube Videos/{yt.title}(AYD).mp4').run()
    #Removing the unwanted files
    os.remove(f'Y:/Youtube Videos/New folder/{yt_v.default_filename}')
    os.remove(f'Y:/Youtube Videos/New folder/{yt_a.title}.mp3')
    print()
    print('Merging was successful & everything worked fine :)')
#Thats it, we are done here
sleep(5)