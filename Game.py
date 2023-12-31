import Agent
from Util import *
from Queries import *
from Params import *
import random
import pygame
from pygame.locals import *
import os
import sys
import math
import cv2
import numpy as np
from Memories import calendar
import asyncio
from multiprocessing import Process
import multiprocessing
import time
import threading
from evaluation_metric import *
from gtts import gTTS
from translate import Translator
import pyautogui
from HoveringBox import *
import textwrap

DEFAULT_IMAGE_SIZE = (WIN_WIDTH, WIN_HEIGHT)
speed = FPS*0.6
translator = Translator(to_lang='ja')


'''
====================
Assests
====================
'''
sheriff_badge = pygame.transform.scale(pygame.image.load('Assets/sheriff_badge.png'), (40,40))
font = pygame.font.SysFont('comicsans', 30, True)
font2 = pygame.font.SysFont('consolas', 25, True)
font3 = pygame.font.Font(None, 40)
bg = pygame.image.load(Path+'town_final_bg.png')
bg_nodes = pygame.image.load(Path+'town_nodes_bg.jpg')
black_bg = pygame.image.load(Path+'blackbg.png')
night_pahse = pygame.image.load('Assets/Phases/Night_Phase.png')
day_phase = pygame.image.load('Assets/Phases/Day_Phase.png')
voting_phase = pygame.image.load('Assets/Phases/Voting Phase.png')
start_phase = pygame.image.load('Assets/Phases/START~2.png')
game_end = pygame.image.load('Assets/Phases/Game_End.png')
werewolves_win = pygame.image.load('Assets/Phases/Werewolves_Win.png')
townfolks_win = pygame.image.load('Assets/Phases/Townfolks_Win.png')
night_phase_japanese = pygame.image.load('Assets/Phases/Night_Phase_Japanese.png')
day_phase_japanese = pygame.image.load('Assets/Phases/Day_Phase_Japanese.png')
voting_phase_japanese = pygame.image.load('Assets/Phases/Voting_Phase_Japanese.png')
townfolks_win_japanese = pygame.image.load('Assets/Phases/Townfolks_Win_Japanese.png')
werewolves_win_japanese = pygame.image.load('Assets/Phases/Werewolves_Win_Japanese.png')
killframes = [pygame.image.load(Path+f'killing/{i}.png') for i in range(N_Killing)]
farewellframesW = [pygame.image.load(Path+f'Farewell/Werewolf/{i}.png') for i in range(N_Farewell_W)]
farewellframesT = [pygame.image.load(Path+f'Farewell/Townfolk/{i}.png') for i in range(N_Farewell_T)]
bgs = [pygame.image.load(Path+f'Background/{i}.png') for i in range(N_Background)]

'''
====================
Button Assests [POPUP]
====================
'''
button_font = pygame.font.Font(None, 24)
button_color = (255, 153, 153) 
house_popup = pygame.transform.scale(pygame.image.load('Assets/house_popup.png'), HOUSE_POPUP_SIZE)
hut_button = pygame.image.load("Assets/button_house.png")
transcript_button = pygame.image.load("Assets/transcript_button.png")
hut_button = pygame.transform.scale(hut_button, POPUP_BUTTON_SIZE)
transcript_button = pygame.transform.scale(transcript_button, POPUP_BUTTON_SIZE)

# Hut 1
hut1_button_x, hut1_button_y =  LOCATION_MAP['Hut 1']
hut1_button_y = hut1_button_y - 50
# Hut 2
hut2_button_x, hut2_button_y =  LOCATION_MAP['Hut 2']
hut2_button_x = hut2_button_x - 20
hut2_button_y = hut2_button_y - 50

# Transcript Button and Popup
transcript_button_x , transcript_button_y = (1800, 40)
transcript_popup = pygame.transform.scale(pygame.image.load('Assets/transcript_box_blue.png'), (600, 800))
transcript_bubble_topleft = (1300, 10)

'''
====================
Fire Animation
====================
'''

# Size of the fire animation
fire_width = FIRE_SIZE[0]
fire_height = FIRE_SIZE[1]
fire_x = FIRE_CENTER[0]
fire_y = FIRE_CENTER[1]
fire_particles = []

for _ in range(100):
    x = random.randint(fire_x, fire_x + fire_width)
    y = random.randint(fire_y, fire_y + fire_height//2)
    dx = random.uniform(-0.1, 0.1)
    dy = random.uniform(-0.2, -0.1)
    size = random.uniform(0.5,1.5)
    fire_particles.append((x, y, dx, dy, size))

fire_animation_frames = [pygame.image.load(f'Assets/Fire/{i}.png') for i in range(40)]
fire_animation_frames.extend(fire_animation_frames[::-1])

current_frame = 0
frame_count = 0
animation_speed = 4  


'''
====================
Emojis
====================
'''

# Load and scale the emoji images
assistant_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "assistant.png"), EMOJI_SIZE)
broom_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "broom.png"), EMOJI_SIZE)
bucket_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "bucket.png"), EMOJI_SIZE)
bulb_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "bulb.png"), EMOJI_SIZE)
cook_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "cook.png"), EMOJI_SIZE)
cow_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "cow.png"), EMOJI_SIZE)
eggs_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "eggs.png"), EMOJI_SIZE)
electricRepair_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "electricRepair.png"), EMOJI_SIZE)
fish_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "fish.png"), EMOJI_SIZE)
fishingPole_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "fishingPole.png"), EMOJI_SIZE)
houseMechanic_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "houseMechanic.png"), EMOJI_SIZE)
houses_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "houses.png"), EMOJI_SIZE)
lamp_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "lamp.png"), EMOJI_SIZE)
pick_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "pick.png"), EMOJI_SIZE)
prayer_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "prayer.png"), EMOJI_SIZE)
shrine_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "shrine.png"), EMOJI_SIZE)
wellMechanic_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "wellMechanic.png"), EMOJI_SIZE)
wood_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "wood.png"), EMOJI_SIZE)
sabotage_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "sabotage.png"), EMOJI_SIZE)
bucket_sabotage_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "bucket_sabotage.png"), EMOJI_SIZE)
broom_sabotage_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "sabotage_broom.png"), EMOJI_SIZE)
fishingpole_sabotage_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "fishingPole_sabotage.png"), EMOJI_SIZE)
fence_sabotage_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "fence_sabotage.png"), EMOJI_SIZE)
cooking_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojiCooking.png"), EMOJI_SIZE)
sleeping_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojiSleeping.png"), EMOJI_SIZE)
reading_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojiReading.png"), EMOJI_SIZE)
reading2_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojiHouseReading2.png"), EMOJI_SIZE)
cleaning_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojiHouseCleaning.png"), EMOJI_SIZE)
house_repair_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojiRepair.png"), EMOJI_SIZE)
bathing_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "emojibathing.png"), EMOJI_SIZE)
electric_maintain = pygame.transform.scale(pygame.image.load(Emoji_Path + "electricRepair.png"), EMOJI_SIZE)
electric_repairWiring = pygame.transform.scale(pygame.image.load(Emoji_Path + "electric_task2.png"), EMOJI_SIZE)
electric_resources = pygame.transform.scale(pygame.image.load(Emoji_Path + "electric_task3.png"), EMOJI_SIZE)
electric_sabotage = pygame.transform.scale(pygame.image.load(Emoji_Path + "electric_sabotage.png"), EMOJI_SIZE)



# Create a dictionary of emojis
EMOJI = {
            #'Eat': eat_emoji,
            'Assistant': assistant_emoji,
            'Broom': broom_emoji,
            'Bucket': bucket_emoji,
            'Bulb': bulb_emoji,
            'Cook': cook_emoji,
            'Cow': cow_emoji,
            'Eggs': eggs_emoji,
            'Electric Repair': electricRepair_emoji,
            'Fish': fish_emoji,
            'Fishing Pole': fishingPole_emoji,
            'House Mechanic': houseMechanic_emoji,
            'Houses': houses_emoji,
            'Lamp': lamp_emoji,
            'Pick': pick_emoji,
            'Prayer': prayer_emoji,
            'Shrine': shrine_emoji,
            'Well Mechanic': wellMechanic_emoji,
            'Wood': wood_emoji,
            'Sabotage': sabotage_emoji,
            'Bucket_Sabotage': bucket_sabotage_emoji,
            'Broom_Sabotage': broom_sabotage_emoji,
            'FishingPole_Sabotage': fishingpole_sabotage_emoji,
            'Fence_Sabotage': fence_sabotage_emoji,
            'Reading_Books': reading2_emoji,
            'Sleeping': sleeping_emoji ,
            'Cooking' : cooking_emoji,
            'Electric Maintain': electric_maintain,
            'Electric Repairing': electric_repairWiring,
            'Electric Resources': electric_resources,
            'Electric_Sabotage':electric_sabotage
        }



'''
====================
Werewolves Game
====================
'''

class Game:
  # Initialize the game
  def __init__(self, agents):
    pygame.font.init()
    pygame.init()
    self.names = [agent.name for agent in agents]
    self.ids = {}
    for i,name in enumerate(self.names):
        self.ids[name] = i

    # WereWolf Game Parameters 
    self.agents = agents
    self.n = len(agents)
    self.alive = [True]*self.n
    self.werewolf = [False]*self.n
    for i in range(self.n):
      if("werewolf" in self.agents[i].summary.split(';')[0]):
         self.werewolf[i] = True
    
    self.w = WIN_WIDTH
    self.h = WIN_HEIGHT
    self.bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)
    self.bg_tasktable = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)
    self.black_bg = pygame.transform.scale(black_bg, DEFAULT_IMAGE_SIZE)
    self.bgs = bgs

    # Backgrounds 
    for i in range(N_Background): 
      self.bgs[i] =  pygame.transform.scale(self.bgs[i], DEFAULT_IMAGE_SIZE) 

    self.fire = True
    self.fps = FPS
    self.killing = False
    self.killId = 0
    self.elim = 0
    self.killframes = killframes

    # Kill Frames
    for i in range(N_Killing): 
      self.killframes[i] =  pygame.transform.scale(self.killframes[i], DEFAULT_IMAGE_SIZE)  
    self.farewell = False
    self.farewellID = 0
    self.farewellframesT = farewellframesT
    self.farewellframesW = farewellframesW

    # Farewell Frames
    for i in range(N_Farewell_T): 
      self.farewellframesT[i] =  pygame.transform.scale(self.farewellframesT[i], DEFAULT_IMAGE_SIZE) 
    for i in range(N_Farewell_W): 
      self.farewellframesW[i] =  pygame.transform.scale(self.farewellframesW[i], DEFAULT_IMAGE_SIZE) 
    
    # Display Parameters 
    self.changePhase = False 
    self.Night = 0
    self.bgId = -1
    self.VelFactor = 1
    self.planNow = None
    self.show_house1 = True
    self.win = pygame.display.set_mode((self.w,self.h),RESIZABLE)
    pygame.display.set_caption("Werewolves of Miller Hollow")
    self.clock = pygame.time.Clock()
    self.InitialPositions = InitialPositions
    self.contexts = {}

    for i in range(self.n):
      self.contexts[self.names[i]] = {}
    self.elimination = None
    self.elim = 0
    self.night_elimination = None
    self.day_phase = pygame.transform.scale(day_phase, DEFAULT_IMAGE_SIZE)
    self.day_phase_japanese = pygame.transform.scale(day_phase_japanese, DEFAULT_IMAGE_SIZE)
    self.night_phase = pygame.transform.scale(night_pahse, DEFAULT_IMAGE_SIZE)
    self.night_phase_japanese = pygame.transform.scale(night_phase_japanese, DEFAULT_IMAGE_SIZE)
    self.voting_phase = pygame.transform.scale(voting_phase, DEFAULT_IMAGE_SIZE)
    self.voting_phase_japanese = pygame.transform.scale(voting_phase_japanese, DEFAULT_IMAGE_SIZE)
    self.townfolks_win = pygame.transform.scale(townfolks_win, DEFAULT_IMAGE_SIZE)
    self.townfolks_win_japanese = pygame.transform.scale(townfolks_win_japanese, DEFAULT_IMAGE_SIZE)
    self.werewolves_win = pygame.transform.scale(werewolves_win, DEFAULT_IMAGE_SIZE)
    self.werewolves_win_japanese = pygame.transform.scale(werewolves_win_japanese, DEFAULT_IMAGE_SIZE)
    self.start_phase = pygame.transform.scale(start_phase, DEFAULT_IMAGE_SIZE)
    self.end_phase = pygame.transform.scale(game_end, DEFAULT_IMAGE_SIZE)
    self.day_phase_show = False
    self.day_phase_japanese_show = True
    self.night_phase_show = False
    self.night_phase_japanese_show = False
    self.voting_phase_show = False
    self.voting_phase_japanese_show = False
    self.townfolks_win_show = False
    self.townfolks_win_japanese_show = False
    self.werewolves_win_show = False
    self.werewolves_win_japanese_show = False
    self.start_phase_show = False
    self.end_phase_show = False
    self.nobodyLynch = False
    self.house1Popup = False
    self.house2Popup = False
    self.transcriptPopup = False
    self.convs = 0
    self.ClockPrev = Clock_Speed
    self.choose_sheriff = False
    self.agent_sheriff = None
    self.chooseSheriff()

    for i in range(self.n):
        if(self.alive[i]):
           self.agents[i].remember(f"{self.agent_sheriff.name} was chosen as the new Sheriff")

    self.HoverBox_agents = {}
    self.reset()

    # Hover Box for Agents
    self.initHover()
    self.playBgMusic()  
    
    # Transcript Code
    self.scroll_offset = 0
    self.scroll_speed = 10
    self.text_content = ['Transcript of Conversations']*2
    for i in range(2):
      self.text_content.append('')
    for i in range(self.n):
      self.agents[i].game = self
    self.tasksDone = 0
    
    self.rememberInit()
    pyautogui.click(500, 500, button='left')
    time.sleep(0.01)
    pyautogui.moveTo(pyautogui.size()[0]-1,0)


  # Thread for Night Phase 
  def rememberInit(self):
    threads = []
    for i in range(self.n):
        thread = threading.Thread(target=self.rememberAgent, args=(i,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
  
  def rememberAgent(self,id):
    for i in range(self.n):
      if(i==id): continue
      self.agents[id].remember(f"About {self.agents[i].name}: {self.agents[i].summary}")
  
  def initHover(self):
    '''
      ====================
      Initializing Agents Hover Box
      ====================
    '''
    for i,agent in enumerate(self.agents):
      init_x,init_y = agent.x,agent.y
      size_x, size_y = 50, 50
      player_rect = pygame.Rect(init_x, init_y, size_x, size_y)
      hover_box_player = HoverTextBox_Agent(player_rect, font, (255, 255, 255), (0, 0, 255), agent, agent.name, agent.summary,"")
      self.HoverBox_agents[agent.name] = hover_box_player


  def getSingleContext(self,name1,name2):
      self.contexts[name1][name2] = self.agents[self.ids[name1]].vote_context(name2)
     
  def getContext(self,name,night=False):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): 
          continue
        if(name==self.names[i]): 
          continue

        # threading for context 
        thread = threading.Thread(target=self.getSingleContext, args=(name, self.names[i],))
        thread.start()
        threads.append(thread)

    # Joining threads
    for thread in threads:
        thread.join()

  # Below code for Text to Speech for Group conversations
  def speak(self,text,curr):
    voicePath = "Assets/voice.mp3"
    translation = translator.translate(text)
    tts = gTTS(translation, lang='ja')
    tts.save(voicePath)
    self.agents[curr].isSpeaking = True
    music = pygame.mixer.music.load(voicePath)
    pygame.mixer.music.play(1)
    while pygame.mixer.music.get_busy():
      time.sleep(0.1)
    pygame.mixer.music.unload()
    self.agents[curr].isSpeaking = False

  # Trigger for Group Conversation between Werewolves  
  def nightVoteWerewolf(self,i,names,history=None):
    voteContext = ""
    sr = 1
    for key, value in self.contexts[self.names[i]].items():
        voteContext += f"{sr}) {key}: {value}\n"
        sr += 1
    if history is None:
      voteName = self.agents[i].brain.query(QUERY_NIGHT_SINGLE.format(self.agents[i].name,voteContext,names),name='QUERY_NIGHT_SINGLE')
    else: 
      voteName = self.agents[i].brain.query(QUERY_NIGHT.format(self.agents[i].name,voteContext,history,names),name='QUERY_NIGHT')
    
    try:
      vote = self.names.index(voteName)
    except:
      voteName = self.findName(voteName,self.names[i])
      vote = self.names.index(voteName)
    
    if(self.werewolf[self.ids[voteName]]):
      vote = random.choice([index for index, value in enumerate(self.werewolf) if value is False and self.alive[index]])
    self.votes[vote] += 1

  
  def sleep(self):
    for i in range(self.n):
      if(not self.alive[i] or self.werewolf[i]): continue
      self.agents[i].sleep()

  def wakeUp(self):
    for i in range(self.n):
      if(not self.alive[i] or self.werewolf[i]): continue
      self.agents[i].sleeping = False
      self.agents[i].task = None
      self.agents[i].taskReach = False

  # Night vote for killing a townfolk
  def nightVote(self):
    self.text_content.append("  ")
    self.text_content.append(" -- NIGHT PHASE -- ")
    self.text_content.append("  ")
    self.threadNight = threading.Thread(target=self.nightVoteContext)
    self.threadNight.start()
    self.night_phase_japanese_show = True
    log("Currently it is Night, the Werewolves will kill a townfolk...\n")
    self.votes = [0]*self.n

    self.sleep()

    names = ""
    j = 1
    werewolves = 0
    for i in range(self.n):
      if(self.werewolf[i] and self.alive[i]): 
        werewolves+=1
      if(self.werewolf[i]): 
        continue
      if(not self.alive[i]): 
        continue
      names = names + f"{j}) {self.names[i]}\n"
      j += 1
    names = names[:-1]
      
    voters = []
    for i in range(self.n):
      if(self.alive[i] and self.werewolf[i]):
        voters.append(i)

    self.assembleTavern(voters)
    context = []
    self.threadNight.join()
    self.threadDay = threading.Thread(target=self.dayVoteContext)
    self.threadDay.start()

    if(werewolves>1):
      for i in range(self.n):
        if(not self.alive[i] or not self.werewolf[i]): context.append("")
        else: 
            voteContext = ""
            sr = 1
            for key, value in self.contexts[self.names[i]].items():
                voteContext += f"{sr}) {key}: {value}\n"
                sr += 1
            context.append(voteContext[:-1])

      global MinDialogues
      MinDialoguesPrev = MinDialogues
      MinDialogues = 4

      conversation = self.groupConversation(context,voters,True)
      MinDialogues = MinDialoguesPrev
      # Thread for nightVoteWerewolf 
      threads = []
      for i in range(self.n):
          if(not self.werewolf[i] or not self.alive[i]): continue
          thread = threading.Thread(target=self.nightVoteWerewolf, args=(i,names,conversation,))
          thread.start()
          threads.append(thread)
      for thread in threads:
          thread.join()
    
    else: 
      for i in range(self.n):
        if(not self.werewolf[i] or not self.alive[i]): continue
        self.nightVoteWerewolf(i,names)
      self.waitAssemble(voters)

    kick = self.votes.index(max(self.votes))
    self.alive[kick] = 0
    self.kicked = self.names[kick]
    self.killing = True
    self.elimination = self.kicked

    if self.agents[kick].sheriff:
      threadSheriff = threading.Thread(target=self.chooseSheriff)
      threadSheriff.start()

    # Thread for addObservationAll 
    threadObs = threading.Thread(target=self.addObservationAll, args=(f"{self.kicked} has been eliminated by the Werewolves on {calendar.day} during the Night Phase",))
    threadObs.start()
    log(f"{self.kicked} has been killed by the Werewolves\n\n")
    self.checkEnd()
    self.wakeUp()

  def addObservationAll(self,observation):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.agents[i].remember, args=(observation,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

  def nightVoteContext(self):
    threads = []
    for i in range(self.n):
        if(not self.alive[i] or not self.werewolf[i]): continue
        thread = threading.Thread(target=self.getContext, args=(self.names[i],True,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join() 

  def dayVoteContext(self):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.getContext, args=(self.names[i],False,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()     

  def dayVote(self):
    self.text_content.append(" -- VOTING PHASE -- ")
    self.text_content.append("  ")
    self.voting_phase_japanese_show = True
    log("Currently it is Day, the Villagers will lynch someone...\n")

    context = []
    voters = []
    for i in range(self.n):
      if(self.alive[i]):
        voters.append(i)

    # Thread for dayVoteContext
    self.assembleTavern(voters)
    self.threadDay.join()

    for i in range(self.n):
       if(not self.alive[i]): context.append("")
       else: 
          voteContext = ""
          sr = 1
          for key, value in self.contexts[self.names[i]].items():
              voteContext += f"{sr}) {key}: {value}\n"
              sr += 1
          context.append(voteContext[:-1])

    conversation = self.groupConversation(context,voters)

    votes = [0]*self.n
    log()
    prev = None
    for i,voteId in enumerate(voters):
      cover = "Werewolf" if self.werewolf[voteId] else "Townfolk"
      names = ""
      j = 1
      for id in voters:
        if(id==voteId): continue
        if(self.werewolf[voteId]):
          idCover = "Werewolf" if self.werewolf[id] else "Townfolk"
          names = names + f"{j}) {self.names[id]} - {idCover}\n"
        else:
          names = names + f"{j}) {self.names[id]}\n"
        j += 1
      names = names[:-1]

      # get the vote name from the agent 
      voteName = self.agents[voteId].brain.query(
         QUERY_DAY.format(self.agents[voteId].name,context[voteId],
                          conversation,self.agents[voteId].name,cover,
                          names,self.agents[voteId].name,self.agents[voteId].name,self.agents[voteId].name),name='QUERY_DAY')
      try:
        vote = self.names.index(voteName)
      except:
        voteName = self.findName(voteName,self.names[voteId])
        vote = self.names.index(voteName)
      log(f"{self.agents[voteId].name} voted to kick out {voteName}")
      threadObs = threading.Thread(target=self.addObservationAll, args=(f"{self.agents[voteId].name} voted to kick out {voteName} on {calendar.day} during the day phase",))
      threadObs.start()
      if(self.agents[voteId].sheriff): votes[vote] += 2
      else: votes[vote] += 1
      if prev is not None: self.agents[prev].isSpeaking = False
      self.agents[voteId].isSpeaking = True
      self.agents[voteId].msg = f"I vote to kick out {voteName}"
      prev = voteId
      time.sleep(0.5)

    # Condtion for Nobody Lynch  
    maxVotes = max(votes)
    if(votes.count(maxVotes)>1):
      log("\nNobody was lynched")
      self.nobodyLynch = True
      threadObs = threading.Thread(target=self.addObservationAll, args=(f"Nobody was lynched on {calendar.day} during the day phase",))
      threadObs.start()
    else:
      kick = votes.index(maxVotes)
      self.alive[kick] = 0
      self.kicked = self.names[kick]

      #If sheriff is kicked
      if self.agents[kick].sheriff:
        threadSheriff = threading.Thread(target=self.chooseSheriff)
        threadSheriff.start()

      self.farewell = True
      self.killing = True
      self.elimination = self.names[kick]
      log()
      log(f"{self.kicked} has been lynched by the Villagers")
      kickedCover = "Werewolf" if self.werewolf[kick] else "Townfolk"
      threadObs = threading.Thread(target=self.addObservationAll, args=(f"{self.kicked} has been lynched on {calendar.day} during the day phase.\n{self.kicked} was a {kickedCover}",))
      threadObs.start()

    for agent in self.agents:
      agent.location_name = 'Tavern'
      agent.dest = None
      agent.isSpeaking = False

    self.checkEnd()
      
  def findName(self,currName,voterName=None):
    for name in self.names:
      if(voterName is not None and name==voterName): continue
      if name in currName or currName in name:
        return name
    for name in self.names:
      if(voterName is not None and name==voterName): continue
      if name.split(' ')[0] in currName:
        return name
    raise Exception(f"Invalid Name - {currName}")

  # Group Conversations between agents for lynching 
  def groupConversation(self, context, voters, night=False):
      history = ""

      if(night):
        remainingTownfolk = getNames(self,True)
        remainingWerewolf = getNames(self,False)
      else:
        remainingTownfolk = getDetails(self)
        remainingWerewolf = getDetails(self,True)         

      curr = random.choice(voters)
      votersN = len(voters)

      if(night):
        reply = self.agents[curr].nightconv_init(context[curr],remainingTownfolk,remainingWerewolf)
      else:
        remaining = remainingWerewolf if self.werewolf[curr] else remainingTownfolk
        reply = self.agents[curr].groupconv_init(self.kicked,context[curr],remaining)

      try:
        replyMsg = extract_dialogue(reply)
      except: 
        replyMsg = reply

      global Clock_Speed

      self.waitAssemble(voters)

      Clock_Speed = 1

      # Thread for speak and group conversation
      thread = threading.Thread(target=self.speak, args=(replyMsg,curr,))
      thread.start()
      self.agents[curr].msg = replyMsg 
      prev = curr
      moderator = GPT()
      names = ""
      for i,name in enumerate([self.agents[i].name for i in voters]):
        names = names + f"{i+1}) " + name + '\n'
      names = names[:-1]
      dialogues = 0
      lastFew = []
      rating = 0 
      rating_n = 0

      # Group Conversation Loop and end condition
      while curr is not None:
          dialogues += 1
          log(reply)
          history = history + reply
          self.text_content.append(reply)
          lastFew.append(reply)
          if(len(lastFew)>4): lastFew.pop(0)
          if(dialogues>MaxDialogues): break
          if(dialogues<MinDialogues): 
            QUERY = QUERY_GROUPCONV_MODERATOR
            queryName = 'QUERY_GROUPCONV_MODERATOR'
          else: 
            QUERY = QUERY_GROUPCONV_MODERATOR_END
            queryName = 'QUERY_GROUPCONV_MODERATOR_END'
          
          if(votersN>2):
            currName = moderator.query(QUERY.format('\n'.join(lastFew[-2:]),names),name=queryName)
            if("End Conversation" in currName): break
            try:
              curr = self.ids[currName]
            except:
              try:
                currName = self.findName(currName)
                curr = self.ids[currName]
              except:
                break
          else:
            EndScore = extractImportance(moderator.query(QUERY_GROUPCONV_END.format('\n'.join(lastFew[-2:])),name='QUERY_GROUPCONV_END'))
            if(dialogues+EndScore>10): break
            if(dialogues==4): break 
            curr = voters[1-voters.index(curr)]
          
          if(night):
            reply = self.agents[curr].nightconv(context[curr], '\n'.join(lastFew[-3:]), remainingTownfolk, remainingWerewolf)
          else:
            remaining = remainingWerewolf if self.werewolf[curr] else remainingTownfolk
            reply = self.agents[curr].groupconv(self.kicked, context[curr], '\n'.join(lastFew[-3:]), remaining)

          if(prev!=curr):
            try:
              rating += getResponseRating(lastFew[-1], reply, self.contexts[self.names[curr]][self.names[prev]], self.names[prev], self.names[curr])
              rating_n += 1
            except:
              pass
          thread.join()
          try:
            replyMsg = extract_dialogue(reply)
          except: 
            replyMsg = reply
          thread = threading.Thread(target=self.speak, args=(replyMsg,curr,))
          thread.start()
          self.agents[curr].msg = replyMsg 
          prev = curr
          history = history + '\n'
          for i in range(self.n):
            if(self.alive[i]): self.agents[i].remember(reply)
      log("\nEnd of Conversation")

      if(rating_n==0): 
        self.convRating = 0
      else:
        self.convRating = rating/rating_n

      # log metrics for group conversation   
      log(f"\nConversation Rating - {self.convRating}")
      log(f"Turn Taking Ratio - {get_turn_taking_ratio(history)}")
      log(f"Response Relevance - {calculate_response_relevance(history)}")
      log(f"Agreement Metric - {calculate_agreement_metric(history)}")
      thread.join() 
      Clock_Speed = self.ClockPrev
      self.playBgMusic()
      return history
  
  def assembleTavern(self, voters):
    n = len(voters)
    for i in range(n):
      self.agents[voters[i]].destination_path = []
      self.agents[voters[i]].dest = "Stop"
    angle = 2 * math.pi / n
    for i in range(n):
      theta = i * angle
      x = TavernCenter[0] + int(TavernRadius * math.cos(theta))
      y = TavernCenter[1] + int(TavernRadius * math.sin(theta))
      
      self.agents[voters[i]].tavern((x,y))

  def waitAssemble(self, voters):
    n = len(voters)
    wait = True 
    while wait:
      wait = False
      for i in range(n):
        if len(self.agents[voters[i]].destination_path)!=0:
          wait = True 
          break
      time.sleep(0.1) 

  def afternoon(self):
    self.text_content.append(" -- MORNING PHASE -- ")
    self.text_content.append("  ")
    self.day_phase_japanese_show = True
    threadPlan = threading.Thread(target=self.generatePlanDay)
    threadPlan.start()   
    planGen = False   
    first = True
    while True:
      if(calendar.dt.hour in [2,14]): break
      if(calendar.dt.minute==0 and calendar.dt.hour%2==0):
        now = calendar.time
        if(not planGen):
           threadPlan.join()
           planGen = True
        self.planNow = now
        threads = []
        for i in range(self.n):
            if(not self.alive[i]): continue
            self.agents[i].task = None
            self.agents[i].taskReach = False
            thread = threading.Thread(target=self.agents[i].nextLocation, args=(now,self,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        self.observe(now)

      time.sleep(0.3)
      
    for i in range(self.n):
      self.agents[i].task = None 
      self.agents[i].taskReach = False 
    self.planNow = None 

  # Code for loading the observations of the agents and updating the memory   
  def observe(self,now=None):
    if(now is None): now = calendar.time
    for i in range(self.n):
        if(not self.alive[i]): continue
        for j in range(self.n):
          if(i==j or not self.alive[j]): continue
          if(self.agents[i].hub == self.agents[j].hub):
            if(self.agents[j].task is not None):
              if(self.agents[j].werewolf and not self.agents[i].werewolf and "Sabotage" in TASK_EMOJI_MAP[self.agents[j].task]):
                self.agents[i].remember(f"{self.agents[i].name} saw {self.agents[j].name} doing a Sabotage Task - {nodes[self.agents[j].task]} at {calendar.time}") 
              else:  
                self.agents[i].remember(f"{self.agents[i].name} saw {self.agents[j].name} {nodes[self.agents[j].task]} at {calendar.time}")  
            if(self.agents[i].task is not None and self.agents[j].task is not None and not self.agents[i].busy and not self.agents[j].busy):  
              threadConv = threading.Thread(target=self.conversation, args=(self.names[i],self.names[j],))
              threadConv.start()   

  # Generate the plan for the agents for the day phase
  def generatePlanDay(self):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.agents[i].generatePlanDay)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

  # Check condtition for game end
  def checkEnd(self):
    while(self.killing or self.elimination is not None):
      time.sleep(0.1)
    players = [0,0]
    for i in range(self.n):
       if(self.alive[i]):
          players[self.werewolf[i]]+=1
    if(players[1]==0):
      log('\n=== TOWNFOLKS WIN ===')
      self.townfolks_win_japanese_show = True
      time.sleep(5)
      self.run = False
      pygame.quit()
    if(players[1]>=players[0] or (not self.Night and players[1]>=players[0])):
      log('\n=== WEREWOLVES WIN ===')
      self.werewolves_win_japanese_show = True
      time.sleep(5)
      self.run = False 
      pygame.quit()
          
    
  def switchPhase(self):
    self.changePhase = True

  # Group conversation between agents based on the parameters defined in the paper
  def conversation(self, name1, name2):
    global Clock_Speed
    self.convs+=1
    names = [name1,name2]
    curr = 0
    agents = [self.agents[self.ids[name1]], self.agents[self.ids[name2]]]
    agents[0].busy = True 
    agents[1].busy = True
    thread1 = threading.Thread(target=self.getSingleContext, args=(name1,name2,))
    thread1.start()
    thread2 = threading.Thread(target=self.getSingleContext, args=(name2,name1,))
    thread2.start()
    thread1.join() 
    thread2.join()
    try:
      observation = f"{agents[curr].name} saw {agents[1-curr].name} {nodes[agents[1-curr].task]} at {calendar.time}"
    except:
      observation = f"{agents[curr].name} saw {agents[1-curr].name} at {calendar.time}"
    reply = agents[curr].talk_init(agents[1-curr].name, observation, self.contexts[names[curr]][names[1-curr]])
    while(not agents[0].taskReach or not agents[1].taskReach):
      time.sleep(0.2)
    if(agents[0].task==agents[1].task):
      agents[0].destination_path = [(agents[0].x-15,agents[0].y+10)]
      agents[1].destination_path = [(agents[1].x+15,agents[1].y-10)]
      agents[0].dest = "Stop"
      agents[1].dest = "Stop"
    Clock_Speed = 1
    try:
      replyMsg = extract_dialogue(reply)
    except: 
      replyMsg = reply
    agents[curr].msg = replyMsg 
    agents[curr].isSpeaking = True
    history = ""
    lastFew = []
    conv_n = 0
    moderator = GPT()
    while reply is not None:
        log(reply)
        lastFew.append(reply)
        conv_n += 1
        EndScore = extractImportance(moderator.query(QUERY_GROUPCONV_END.format('\n'.join(lastFew[-2:])),name='QUERY_GROUPCONV_END'))
        if(conv_n+EndScore>10): break
        history = history + '\n' + reply
        self.text_content.append(reply)
        curr = 1 - curr
        reply = agents[curr].talk(agents[1-curr].name, reply, '\n'.join(lastFew[-3:]), self.contexts[names[curr]][names[1-curr]], conv_n)
        if(reply is None): break
        try:
          replyMsg = extract_dialogue(reply)
        except: 
          replyMsg = reply
        agents[curr].msg = replyMsg 
        agents[1-curr].isSpeaking = False
        agents[curr].isSpeaking = True
        history = history + '\n'
    log("\nEnd of Conversation")
    self.text_content.append(" -- END OF CONVERSATION -- ")
    self.text_content.append("   ")
    self.convs-=1
    agents[0].isSpeaking = False 
    agents[1].isSpeaking = False 
    agents[0].busy = False 
    agents[1].busy = False
    if(agents[0].task==agents[1].task):
      agents[0].destination = agents[0].task
      agents[1].destination = agents[1].task
    if(not self.convs): Clock_Speed = self.ClockPrev

  def reset(self) : 
      for agent in self.agents:
         agent.graphics_init(self.win)
      self.run = True

  def draw_time(self) :
      timePrecise = calendar.dt.strftime("%I:%M:%S %p")
      text = f"{calendar.day}\n{timePrecise}"
      position = (10,10)
      margin = 1
      # Split the text into lines
      text_lines = text.splitlines()

      line_height = font2.get_linesize()
      y = position[1]

      for line in text_lines:
          text_surface = font2.render(line, True, BLACK)
          text_rect = text_surface.get_rect()
          text_rect.topleft = (position[0]+margin, y+margin)
          pygame.draw.rect(self.win, WHITE, (position[0], y, text_rect.width+2*margin, text_rect.height+2*margin))
          self.win.blit(text_surface, text_rect)
          y += line_height

  def stepKilling(self):
      if(self.fire): 
        self.fire = False
      n = N_Killing
      if(self.farewell):
        if(self.werewolf[self.ids[self.kicked]]):
          n = N_Farewell_W 
        else: 
          n = N_Farewell_T
      if(self.killId==n*Speed_Killing):
          self.killing = False
          self.farewell = False
          self.killId = 0
          if(self.Night):
            self.bg = self.bgs[0]
          else:
            self.bg = self.bgs[N_Background-1] 
          self.fire = True
      else:
        if(self.farewell):
          if(self.werewolf[self.ids[self.kicked]]):
              self.bg = self.farewellframesW[self.killId//Speed_Killing]
          else:
              self.bg = self.farewellframesT[self.killId//Speed_Killing]
        else:
          self.bg = self.killframes[self.killId//Speed_Killing]
        self.killId+=1

  def playBgMusic(self):
    music = pygame.mixer.music.load(Path+'music.mp3')
    pygame.mixer.music.play(-1)
     
  
  def stepPhase(self):
    if(not self.Night):
      if(self.bgId==0):
          self.changePhase = False
          self.bgId=-1
          self.Night = True
      else:
          if(self.bgId==-1): self.bgId=N_Background
          self.bgId-=1
          self.bg = self.bgs[self.bgId]
    else:
      if(self.bgId==N_Background-1):
          self.changePhase = False
          self.bgId=-1
          self.Night = False
          self.bg = self.bg_tasktable
      else:
          self.bgId+=1
          self.bg = self.bgs[self.bgId]

  #---------------------------------- DRAWING FUNCTIONS ----------------------------------#
  def drawTaskEmoji(self):
    for i in range(self.n):
      if(not self.alive[i]): continue
      if self.agents[i].taskReach and not self.agents[i].inPopup_house1 and not self.agents[i].inPopup_house2:
         self.agents[i].emoji_bubble(TASK_EMOJI_MAP[self.agents[i].task])

  def drawTaskEmoji_InsidePopup(self, name):
    for i in range(self.n):
      if(not self.alive[i]): continue
      if name == 'Hut 1':
        if self.agents[i].taskReach and self.agents[i].inPopup_house1:
          self.agents[i].emoji_bubble(TASK_EMOJI_MAP[self.agents[i].task])
      elif name == 'Hut 2':
        if self.agents[i].taskReach and self.agents[i].inPopup_house2:
          self.agents[i].emoji_bubble(TASK_EMOJI_MAP[self.agents[i].task])
         
  def drawElimination(self):

      if(self.elim==0):
        self.bg = self.black_bg
        self.win.blit(self.bg,(0,0))
        self.text1 = self.elimination + " has been Killed"
        if(self.werewolf[self.ids[self.elimination]]):
          self.text2 = self.elimination + " was a Werewolf"
        else: self.text2 = self.text2 = self.elimination + " was a Townfolk"
        self.elimination = self.agents[self.ids[self.elimination]]
        self.elimination.animationKillInit()
        self.elim = 1
        return 

      if(self.elimination.kill_x > WIN_WIDTH):
        self.elimination = None 
        self.elim = 0
        if(self.Night):
          self.bg = self.bgs[0]
        else:
          self.bg = self.bgs[99] 
        return
      
      text_surface = font2.render(self.text1, True, WHITE)
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = WIN_HEIGHT // 4
      self.win.blit(text_surface,text_rect)

      text_surface = font2.render(self.text2, True, WHITE)
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = 3*WIN_HEIGHT // 4
      self.win.blit(text_surface,text_rect)
      
      self.elimination.animationKillStep()

  
  def draw_nobody_lynch(self) :
      if(not self.nobodyLynch): return
      self.win.blit(self.black_bg,(0,0))
      text_surface = font2.render("Nobody was Lynched", True, WHITE)
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = WIN_HEIGHT // 2
      self.win.blit(text_surface,text_rect)
      self.nobodyLynch = False
      pygame.display.update()
      time.sleep(3)  

  # Choose sheriff at starting of the game
  def new_sheriff_choose(self) :
      if(not self.choose_sheriff or self.agent_sheriff is None): return
      self.win.blit(self.black_bg,(0,0))
      text_surface = font2.render(f"{self.agent_sheriff.name} was chosen as the new Sheriff", True, WHITE)

      for i in range(self.n):
        if(self.alive[i]):
           self.agents[i].remember(f"{self.agent_sheriff.name} was chosen as the new Sheriff")
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = WIN_HEIGHT // 2
      self.win.blit(text_surface,text_rect)
      self.choose_sheriff = False
      pygame.display.update()
      time.sleep(3)     
  
  def draw_coordinates(self):
    dot_radius = 3
    for name, coord in LOCATION_MAP.items():
        x, y = coord
        if('Hut 1' in name):
          pygame.draw.circle(self.win, RED, (x, y), dot_radius)
        if('Hut 2' in name):
          pygame.draw.circle(self.win, BLUE, (x, y), dot_radius)


  def draw_fps(self):
    self.fps = int(self.clock.get_fps())
    fps_text = font3.render(f"FPS: {self.fps}", True, (0, 85, 255))
    fps_text_rect = fps_text.get_rect(bottomright=(10+fps_text.get_width(), self.win.get_height() - 10))
    self.win.blit(fps_text, fps_text_rect)
    if(self.fps>15): self.VelFactor = FPS/self.fps

  def draw_popup(self):
    # Get the rect of the image
    if(self.house1Popup==True):
      image_rect = house_popup.get_rect()
      image_rect.center = (hut1_button_x, hut1_button_y)
      self.win.blit(house_popup, image_rect)
    elif(self.house2Popup==True):
      image_rect = house_popup.get_rect()
      image_rect.center = (hut2_button_x, hut2_button_y)
      self.win.blit(house_popup, image_rect)  

    if(self.transcriptPopup):
      image_rect = transcript_popup.get_rect()
      image_rect.topleft = transcript_bubble_topleft
      font_size = 22
      font = pygame.font.Font(None, font_size)
      # maximum of 6 words per line
      text_lines = []
      
      for reply in self.text_content:
        line = ""
        words = reply.split()
        for word in words:
            if len(line.split()) < 9:
                line += " " + word
            else:
                text_lines.append(line.strip())
                line = word
        text_lines.append(line.strip())


      text_height = len(text_lines) * font.get_linesize()

      # Update the scrolling offset to stay within the text boundaries
      max_scroll = max(0, text_height - transcript_rect_height)
      self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

      # Blit the transcript_popup image on top of the background surface
      self.win.blit(transcript_popup, image_rect)

      # Blit the visible portion of the text directly onto 'self.win'
      current_y = -self.scroll_offset
      for line in text_lines:
        text_surface = font.render(line, True, BLACK)
        if current_y > 0 and current_y < 600:
          
          self.win.blit(text_surface, (image_rect.left+70, image_rect.top+110 + current_y))
        current_y += font.get_linesize()

  def draw_agent_in_popup(self,name):
    if(name == 'Hut 1'):
     for i,player in enumerate(self.agents): 
          if(self.alive[i] and player.inPopup_house1):
              player.draw()
    elif(name == 'Hut 2'):
     for i,player in enumerate(self.agents): 
          if(self.alive[i] and player.inPopup_house2):
              player.draw() 

  def draw_window(self) : 

    if(self.werewolves_win_japanese_show):
      self.win.blit(self.werewolves_win_japanese,(0,0))
      pygame.display.update()
      return
    if(self.townfolks_win_japanese_show):
      self.win.blit(self.townfolks_win_japanese,(0,0))
      pygame.display.update()
      return

    self.win.blit(self.bg,(0,0))

    if(self.elimination is not None and not self.killing):
      self.drawElimination()

    if(self.choose_sheriff):
       self.new_sheriff_choose()

    if(not self.killing and self.elimination is None):

      self.draw_nobody_lynch()
      self.draw_phase()
      

      for i,player in enumerate(self.agents): 
          if(self.alive[i] and not player.inPopup_house1 and not player.inPopup_house2):
              player.draw() 
      self.draw_fire()
      for i,player in enumerate(self.agents): 
          if(self.alive[i] and not player.inPopup_house1 and not player.inPopup_house2):
              player.drawBubble() 

      self.drawTaskEmoji()

      self.draw_time()
      self.draw_fps()
      self.draw_static_hover()
      self.draw_hover_agents()
      self.draw_taskbar()

      self.move_hover_box()
      
      
      if(self.house1Popup):
         self.draw_popup()
         self.draw_agent_in_popup('Hut 1')
         self.drawTaskEmoji_InsidePopup('Hut 1')

         for i,player in enumerate(self.agents): 
          if(self.alive[i] and player.inPopup_house1):
              player.drawBubble() 
         self.draw_hover_agents_insidePopup('Hut 1')

         
      elif(self.house2Popup):
         self.draw_popup()
         self.draw_agent_in_popup('Hut 2')
         self.drawTaskEmoji_InsidePopup('Hut 2')
         for i,player in enumerate(self.agents): 
          if(self.alive[i] and player.inPopup_house2):
              player.drawBubble() 
         self.draw_hover_agents_insidePopup('Hut 2')

      if(self.transcriptPopup):
        self.draw_popup()
      
      self.draw_button() 
      
    pygame.display.update()


  def move_hover_box(self):
     for key in self.HoverBox_agents:
        agent = self.agents[self.ids[key]]
        self.HoverBox_agents[key].update_position(agent.x, agent.y)
        if self.planNow is not None and agent.plan is not None:
          self.HoverBox_agents[key].plans = agent.nextHourPlan(self.planNow)
        
  def draw_fire(self):
    global current_frame, frame_count, animation_speed
    # Update fire particles
    for i in range(len(fire_particles)):
        x, y, dx, dy, size = fire_particles[i]
        x += dx
        y += dy
        size -= 0.01
        if size <= 0:
            fire_particles[i] = (random.randint(fire_x, fire_x + fire_width),
                                 random.randint(fire_y, fire_y + fire_height//2),
                                 random.uniform(-0.1, 0.1),
                                 random.uniform(-0.2, -0.1),
                                 random.uniform(0.5,1.5))
        else:
            fire_particles[i] = (x, y, dx, dy, size)

    # Draw central fire
    fire_image = pygame.transform.scale(fire_animation_frames[current_frame], (fire_width, fire_height))
    self.win.blit(fire_image, (fire_x, fire_y))

    # Update fire animation frames
    frame_count += 1
    if frame_count >= animation_speed:
        current_frame = (current_frame + 1) % len(fire_animation_frames)
        frame_count = 0

    # Draw fire particles
    for x, y, _, _, size in fire_particles:
        if size > 0:
            pygame.draw.circle(self.win, YELLOW, (int(x), int(y)), int(size))
            
  def draw_taskbar(self):
    progressWidth = (self.tasksDone/TasksWin) * TasksBarWidth
    progressWidth = max(0,progressWidth)
    if(progressWidth>=TasksBarWidth):
      log('\n=== TOWNFOLKS WIN ===')
      self.townfolks_win_japanese_show = True
      time.sleep(5)
      self.run = False
      pygame.quit()
    pygame.draw.rect(self.win, BLACK, (TaskBarX, TaskBarY, TasksBarWidth, TasksBarHeight), 2)
    pygame.draw.rect(self.win, (34, 139, 24), (TaskBarX+2, TaskBarY+2, progressWidth-4, TasksBarHeight-4))
    text_surface = font2.render(f"Tasks Progress", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (math.ceil(TaskBarX + TasksBarWidth/2), math.ceil(TaskBarY + TasksBarHeight/2))
    self.win.blit(text_surface, text_rect)
  
  def draw_button(self):
      button_radius = 25

      if(not hover_dict['Electricity House'].hovered):
        # Hut 1
        button_center1 = (hut1_button_x + button_radius, hut1_button_y + button_radius)
        pygame.draw.circle(self.win, button_color, button_center1, button_radius)
        hut_button_rect = hut_button.get_rect(center=button_center1)
        self.win.blit(hut_button, hut_button_rect)

      #Hut 2
      button_center2 = (hut2_button_x + button_radius, hut2_button_y + button_radius)
      pygame.draw.circle(self.win, button_color, button_center2, button_radius)
      hut_button_rect = hut_button.get_rect(center=button_center2)
      self.win.blit(hut_button, hut_button_rect)

      #Transcript Window
      button_center3 = (transcript_button_x + button_radius, transcript_button_y + button_radius)
      pygame.draw.circle(self.win, button_color, button_center3, button_radius)
      transcript_button_rect = transcript_button.get_rect(center=button_center3)
      self.win.blit(transcript_button, transcript_button_rect)



  def draw_phase(self):
      if(self.night_phase_japanese_show):
        self.win.blit(self.night_phase_japanese,(0,0))
        self.night_phase_japanese_show = False
        calendar.night()
      elif(self.day_phase_japanese_show):
        self.win.blit(self.day_phase_japanese,(0,0))
        self.day_phase_japanese_show = False
        if(calendar.dt.hour>20): calendar.nextDay()
        calendar.tasks()
      elif(self.voting_phase_japanese_show):
        self.win.blit(self.voting_phase_japanese,(0,0))
        self.voting_phase_japanese_show = False
        if(calendar.dt.hour>20): calendar.nextDay()
        calendar.voting()
      elif(self.start_phase_show):
        self.win.blit(self.start_phase,(0,0))
        self.start_phase_show = False
      elif(self.townfolks_win_japanese_show):
        self.win.blit(self.townfolks_win_japanese,(0,0))
        self.townfolks_win_japanese_show = False
      elif(self.werewolves_win_japanese_show):
        self.win.blit(self.werewolves_win_japanese,(0,0))
        self.werewolves_win_japanese_show = False
      elif(self.end_phase_show):
        self.win.blit(self.end_phase,(0,0))
        self.end_phase_show = False
      else:
         return
      pygame.display.update()
      time.sleep(4)
      
  def draw_hover_agents(self):
    for key in self.HoverBox_agents:
      if self.HoverBox_agents[key].hovered and not agentMap[key].inPopup_house1 and not agentMap[key].inPopup_house2 and self.alive[self.ids[key]]:
        self.HoverBox_agents[key].hover_bubble(self.win)
        
  def draw_hover_agents_insidePopup(self,name):
    for key in self.HoverBox_agents:
      if self.HoverBox_agents[key].hovered and agentMap[key].inPopup_house1 and name == 'Hut 1' and self.alive[self.ids[key]]:
        self.HoverBox_agents[key].hover_bubble(self.win)
      elif self.HoverBox_agents[key].hovered and agentMap[key].inPopup_house2 and name == 'Hut 2' and self.alive[self.ids[key]]:
        self.HoverBox_agents[key].hover_bubble(self.win)
        
  def draw_static_hover(self):
    for key in hover_dict:
      if hover_dict[key].hovered:
        hover_dict[key].hover_bubble(self.win)

  def nextDay(self):
     calendar.nextDay()
     calendar.dt = calendar.dt.replace(hour=7, minute=30)
     
  def handleHovers(self,event):
    for key in hover_dict:
      hover_dict[key].handle_event(event)

    for key in self.HoverBox_agents:
      self.HoverBox_agents[key].handle_event(event)
      
  def is_button_clicked(self,mouse_pos):
    if hut1_button_x <= mouse_pos[0] <= hut1_button_x + 50 and hut1_button_y <= mouse_pos[1] <= hut1_button_y + 50:
        self.house1Popup = not self.house1Popup
    if hut2_button_x <= mouse_pos[0] <= hut2_button_x + 50 and hut2_button_y <= mouse_pos[1] <= hut2_button_y + 50:
        self.house2Popup = not self.house2Popup
    if transcript_button_x <= mouse_pos[0] <= transcript_button_x + 50 and transcript_button_y <= mouse_pos[1] <= transcript_button_y + 50:
        self.transcriptPopup = not self.transcriptPopup

  def exit_agent_popup(self, agent, node):
     agent.x,agent.y = LOCATION_MAP[node]
     agent.destination = node
     agent.location_name = node
  
  def check_agent_in_popup(self):
     for agent in self.agents:
        if agent.destination == "Hut 1 Main":
          self.exit_agent_popup(agent, 'Hut 1 Main')
          agent.inPopup_house1 = True
        if agent.destination == "Hut 1":
          self.exit_agent_popup(agent, 'Hut 1')
          agent.inPopup_house1 = False

        if agent.destination == "Hut 2 Main":
          self.exit_agent_popup(agent, 'Hut 2 Main')
          agent.inPopup_house2 = True
        if agent.destination == "Hut 2":
          self.exit_agent_popup(agent, 'Hut 2')
          agent.inPopup_house2 = False
  
  def step(self) :
      for event in pygame.event.get():
        if event.type == pygame.QUIT : 
          self.run = False
          pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
          mouse_pos = pygame.mouse.get_pos()
          self.is_button_clicked(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.scroll_offset -= self.scroll_speed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.scroll_offset += self.scroll_speed
     
        self.handleHovers(event) 
      
      keys = pygame.key.get_pressed()
      self.check_agent_in_popup()
      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
              player.move(self.VelFactor) 
      
      if(self.changePhase):
        self.stepPhase()
      if(self.killing):
        self.stepKilling()

      self.draw_window()
      calendar.increment(self.VelFactor*Clock_Speed/FPS)

  def chooseSheriff(self):
    if(self.agent_sheriff is None):
      townfolks = []
      for i, agent in enumerate(self.agents):
        if self.alive[i] and agent.werewolf == False:
            townfolks.append(agent)
      sheriff = random.choice(townfolks)
      sheriff.sheriff = True
      self.agent_sheriff = sheriff   
      return  

    # Choose next sheriff after the current sheriff is killed  
    names = ""
    j = 1
    for i in range(self.n):
      if(not self.alive[i]): continue
      names = names + f"{j}) {self.names[i]}\n"
      j += 1
    names = names[:-1]

    voteName = self.agent_sheriff.brain.query(
        QUERY_SHERIFF.format(names),name='QUERY_SHERIFF')
    try:
      vote = self.names.index(voteName)
    except:
      voteName = self.findName(voteName,self.agent_sheriff.name)
      vote = self.names.index(voteName)

    sheriff = self.agents[vote]
    sheriff.sheriff = True  
    log(f"{self.agent_sheriff.name} chose {sheriff.name} to be the next Sheriff")

    self.agent_sheriff = sheriff
    self.choose_sheriff = True

        
  def checkSpeakingProximity(self):
      for player1 in self.agents:
          for player2 in self.agents:
              if(player1!=player2):
                  if(abs(player1.x - player2.x) <100 and abs(player1.y - player2.y) < 100):
                      player1.isSpeaking = True
                      player2.isSpeaking = True
                  else:
                      player1.isSpeaking = False
                      player2.isSpeaking = False
    
                  
                
   