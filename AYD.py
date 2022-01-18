#Importing useful and essential libraries
import timeit
from pytube import YouTube
from pytube import Playlist
from time import sleep
start_time=timeit.default_timer()
import pytube.request
import getpass
user=str(getpass.getuser())
import os
import ffmpeg
import http.client

pytube.request.default_range_size = 1048576 # 1MB chunk size

COMPLETED=True
def completed(artist, song_name):
    if COMPLETED==True:
        print(f"\n {status.default_filename} Downloaded successfully\n enjoy :)\n")
    else:
        print('\nPart 1 (Audio) downloaded successfuly')
        print('Startin Part 2 (Video) ....\n')

def progress_bar(self, chunk, bytes_remaining):
    print(f"{round(bytes_remaining*0.000001)} MB remaining")

#Getting the link from user, and then diagnosis the link if its the single video URL or a whole playlist
PLAYLIST=False
while True:
    link = input('\n Please enter the youtube link : ')
    try:
        ytp=Playlist(link)
        ans=input((f'\n {ytp.title} found! press anything to continue (press "N" or "n" if it\'s not what you want)'))
        PLAYLIST=True
        if ans not in ('No','no','N','n'): break
        else: continue
    except:
        pass
    try:
        yts=YouTube(link,on_progress_callback=progress_bar,on_complete_callback=completed)
        ans=input((f'\n {yts.title} found! press anything to continue (press "N" or "n" if it\'s not what you want)'))
        if ans not in ('No','no','N','n'): break
        else: continue
    except:
        print('\n link is not valid, try again')

#Specifying the user desired media format (Video or Audio)
def stat():
    global status
    status = input('\n Audio or video ? (audio=1 \ video=2) ')
    print(' Working.....please be patient')
    return status
while stat() not in ('1', '2'):
        print(' --{} Unknown status, please choose 1 or 2 {}--'.format(3*"\N{Cross Mark}",3*"\N{Cross Mark}")) 

if PLAYLIST:
    numoo = 0
    #Only download the audio for all the URL in a Playlist
    if status == '1' :
        print(f'The number of songs are {ytp.length}')
        for url in ytp.videos:
            singer_name=url.author.replace(" - Topic",'')
            path = f'C:/Users/{user}/Desktop/AYD/{singer_name}/{ytp.title}'
            file_name = url.title + '.mp3'
            try:
                url.streams.get_audio_only().download(output_path = path , filename = file_name)
                numoo +=1
            except http.client.IncompleteRead:
                print('Network Error, please check your internet connection and then try again')    
            except:
                print(' {} didnt download!, please try again'.format(url.title))
                continue
            print(f'\n {url.title} downloaded successfully {ytp.length}/{numoo}')
    #download the video for all the URL in a Playlist
    elif status == '2':
        print(f'The number of videos are {ytp.length}')
        path = f'C:/Users/{user}/Desktop/AYD/{ytp.title}'
        for url in ytp.video_urls:
            yt = YouTube(url,on_progress_callback=progress_bar,on_complete_callback=completed)
            status=yt.streams.filter(file_extension='mp4').get_by_resolution('720p')
            print(f'\t File size -> {round(status.filesize*0.000001)} MB\n\tFile name -> {status.title}')
            try:
                file_name = status.default_filename 
                status.download(output_path = path ,filename = file_name)
                print('\n You getting 720p resolution')
                numoo +=1
            except AttributeError :
                status=yt.streams.filter(file_extension='mp4').get_highest_resolution()
                file_name = status.default_filename
                status.download(output_path = path ,filename = file_name)
                print('\n You getting as high as possible resolution')
                numoo +=1
            except http.client.IncompleteRead:
                print('Network Error, please check your internet connection and then try again')
            except:
                print(' {} didnt download!'.format(status.title))
            print(f'\n {status.title} downloaded successfully {ytp.length}/{numoo}\n')
    print(f'\n All playlist {ytp.title} downloaded !')
    status = None

#The best available Audio


#If the user only want the audio
if status == '1':
    file_name = Audio.title+ '.mp3'
    print(f'\t File size -> {round(Audio.filesize*0.000001)} MB\n\tFile name -> {file_name}')
    singer_name=yts.author.replace(" - Topic",'')
    path = f'C:/Users/{user}/Desktop/AYD/{singer_name}'
    status =  Audio
    status.download(output_path = path ,filename = file_name)

#if the user want the video
elif status == '2':
    path=f'C:/Users/{user}/Desktop/AYD'

    y=yts.streams.filter(file_extension='mp4',type="video")

    res_func=lambda x : x.resolution
    str2flt=lambda x : float(x.replace('p','.0'))
    flt2str=lambda x : str(x).replace('.0','p')
    reslist=list(set(map(res_func,y)))
    reslist=sorted(list(map(str2flt,reslist)),reverse=True)
    reslist=list(map(flt2str,reslist))

    Audio=yts.streams.filter(only_audio=True,adaptive=True)
    
    abr_func=lambda x : x.abr
    str2flt=lambda x : float(x.replace('kbps','.0'))
    flt2str=lambda x : str(x).replace('.0','kbps')
    abrlist=list(set(map(abr_func,Audio)))
    abrlist=sorted(list(map(str2flt,abrlist)),reverse=True)
    abrlist=list(map(flt2str,abrlist))
    Audio=yts.streams.filter(only_audio=True,adaptive=True,abr=abrlist[0])
    Audio=Audio.get_by_itag(Audio[0].itag)

    num=1
    banner='\nPlease choose the resolution :'
    banner_flag=True
    for r in reslist : 
        if banner_flag: print(banner);banner_flag=False
        ytd=yts.streams.filter(file_extension='mp4',type='video',res=r)[0]
        if r in ['720p','360p'] : a_size=0 ; a= 'Recommended'
        else : a_size=Audio.filesize ; a= ' '
        print(f'{num} --> {r}  {round((ytd.filesize+a_size)*0.000001)} MB {a}')
        num += 1

    while True:
        quality=input('$ ')
        try:
            status=yts.streams.filter(file_extension='mp4',type='video',res=reslist[int(quality)-1])[0]
            if status.is_progressive:status.download(output_path=path,filename=status.default_filename);sleep(5);exit()
            else:
                path=f'C:/Users/{user}/AYD'
                COMPLETED=False
                print('Be aware that High quality takes a little time...\n \
                the audio & video must download separately and then they will merge together \ '
                'with ffmpeg and after creating new mp4 file , they will be removed\n');sleep(2)
                Audio.download(output_path=path,filename=Audio.title + '.mp3')
                status.download(output_path=path,filename=status.default_filename)
                COMPLETED=True
                break
        except ValueError:
            print('Invalid input, please enter a integer number')
        except IndexError:
            print(f'Invalild input, you must enter a number between 1 {len(reslist)} ')
        except http.client.IncompleteRead:
            print('Network Error, check your internet connection and try again')

    #Merging audio & video into one single mp4 file with the help of ffmpeg
    input_video = ffmpeg.input(f'C:/Users/{user}/AYD/{status.default_filename}')
    input_audio = ffmpeg.input(f'C:/Users/{user}/AYD/{Audio.title}.mp3')
    f_name=status.default_filename.replace('.mp4','-')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'C:/Users/{user}/AYD/{f_name}(AYD).mp4').run()
    #Removing the unwanted files
    os.replace(f'C:/Users/{user}/AYD/{f_name}(AYD).mp4' , f'C:/Users/{user}/Desktop/AYD/{f_name}(AYD).mp4')
    os.remove(f'C:/Users/{user}/AYD/{status.default_filename}')
    os.remove(f'C:/Users/{user}/AYD/{Audio.title}.mp3')
    os.rmdir(path)
    print()
    print('Merging was successful & everything worked fine :)')
print('------------------------------------------------------------')
print(timeit.default_timer() - start_time)
#Thats it, we are done here