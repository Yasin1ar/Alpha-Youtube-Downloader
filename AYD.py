from pytube import YouTube
from pytube import Playlist
from time import sleep
import pytube.request
pytube.request.default_range_size = 1048576 # 1MB chunk size

def completed(artist, song_name):
    print(f"\n {status.default_filename} Downloaded sucsessfuly\n enjoy :)")

def progress_bar(chunk,_fifromle_handle,bytes_remaining):
    print(f"{round(bytes_remaining*0.000001)} MB remaining")

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

def stat():
    global status
    status = input('\n Audio or video ? (audio=1 \ video=2) ')
    return status
while stat() not in ('1', '2'):
        print(' --{} Unknown status, please choose 1 or 2 {}--'.format(3*"\N{Cross Mark}",3*"\N{Cross Mark}")) 

def vq_available(res):
    global available
    available = yt.streams.filter(file_extension='mp4').get_by_resolution(res)
    if available:
        return f"Available \N{check mark} ({round(available.filesize*0.000001)} MB)" 
    else:
        return "Not available \N{Cross Mark}"

def video_quality():
    quality = input(f'\n Please choose the resolution ( Note : if you press somthing else, default will be 720p ) \
                    \n 1 -> 1080p {vq_available("1080p")}\n 2 -> 720p {vq_available("720p")} \
                    \n 3 -> 480p {vq_available("480p")}\n 4 -> 360p {vq_available("360p")} \
                    \n 5 -> 240p {vq_available("240p")}\n $ ')

    resolution = {'1':'1080p','2':'720p','3':'480p','4':'360p','5':'240p'}
    res = '720p' 
    if quality in resolution.keys() : res = resolution[quality]
    if quality in ('n','N'): quit()
    return res
try:
    if Playlist(link):
        numoo = 0
        if status == '1' :
            print(f'The number of songs are {ytp.length}')
            for url in ytp.videos:
                singer_name=url.author.replace(" - Topic",'')
                path = f'Y:\Music\YD\{singer_name}\{ytp.title}'
                file_name = url.title + '.mp3'
                try:
                    url.streams.get_audio_only().download(output_path = path , filename = file_name)
                    numoo +=1
                except:
                    print(' {} didnt download!'.format(url.title))
                    continue
                print(f'\n {url.title} downloaded sucsessfuly {ytp.length}/{numoo}')

        elif status == '2':
            print(f'The number of videos are {ytp.length}')
            path = f'P:\Youtube Videos\{ytp.title}'
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
                print(f'\n {status.title} downloaded sucsessfuly {ytp.length}/{numoo}')
        print(f'\n All playlist {ytp.title} downloaded !')
        status = None
except:
    pass

if status == '1':
    audio = yts.streams.get_audio_only()
    print(f'\t File size -> {round(audio.filesize*0.000001)} MB\n\tFile name -> {audio.default_filename}')
    status =  audio
    file_name = status.default_filename + '.mp3'
    singer_name=yts.author.replace(" - Topic",'')
    path = f'Y:\Music\YD\{singer_name}'
    status.download(output_path = path ,filename = file_name)

elif status == '2':
    yt=yts
    while True:
        if vq_available(video_quality()):
            print(f'\t File size -> {round(available.filesize*0.000001)} MB\n\tFile name -> {available.default_filename}')
            status = available
            file_name = status.default_filename
            path = 'P:\Youtube Videos'
            status.download(output_path = path ,filename = file_name)
            break
        else:
            print(' This resolution is not available :( try another resolution\n')
sleep(10)