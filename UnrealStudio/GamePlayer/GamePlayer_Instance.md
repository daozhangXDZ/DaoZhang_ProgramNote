# Game Instance, Custom Game Instance For Inter-Level Persistent Data Storage

2019年3月2日

20:04

 

**Author** [Rama](https://wiki.unrealengine.com/index.php?title=User:Rama) ([talk](https://wiki.unrealengine.com/index.php?title=User_talk:Rama))

One of the new UE4 engine features as of 4.4 is the Game Instance class!

This is a globally accessible instanced UObject that can store any data you want to be carried between levels!

Where formally you would have had to write out data to a config file or to binary file, to transfer between levels, now you can use the Game Instance class!

API documentation: [Template:Documentation/Class](https://wiki.unrealengine.com/index.php?title=Template:Documentation/Class&action=edit&redlink=1)

Solus Example

As a realistic example, in Solus there is a Comms Tower that needs to be in the same state when loaded into different levels, as it is seen from a great distance.

The player can perform actions that evolve the state of the Comms Tower, and those changes have to be reflected in each level that the player enters.

Using the Game Instance class, I can record the state of the Comms Tower any time the player makes modifications to it, and carry that information over when the player transitions to a new level!

Then, whenever the player saves the game, I can still save the Comms Tower normally, but a significant amount of management has been eased out of binary file manipulations thanks to the Game Instance class.

Example For You

Here's an example we can do together!

We'll make a custom Game Instance class, and increment an int32 in the tick function of our player controller class.

Then you can watch as you change to several different maps in your own game (console -> open mapname), and you will see we'll have a record of the total ticks that have occurred, even between the different levels!

SolusGameInstance.h

Please note the essential include!

Also note you could access the Game Instance var in blueprints, by using the BP node to Get Game Instance and casting to your custom Game Instance Class!

*/**
         *By Rama*
 **/*

\#pragma once

*//Essential Include*
 \#include *"Engine/GameInstance.h"* 

\#include *"SolusGameInstance.generated.h"*

UCLASS()
 **class** **USolusGameInstance** : **public** UGameInstance
 {
         GENERATED_BODY()
 **public**:
      USolusGameInstance(**const** FObjectInitializer& ObjectInitializer);

*/** Increment this value in any map, change map, and notice it persists! \*/*
         UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=SolusHUDCrosshair)
         int32 InterLevelPersistentValue; 
         
 };

SolusGameInstance.cpp

\#include *"Solus.h"*
 \#include *"SolusGameInstance.h"*

USolusGameInstance::USolusGameInstance(**const** FObjectInitializer& ObjectInitializer)
         : Super(ObjectInitializer)
 {
         
 }

PlayerController.cpp

As you can see below, every Actor.h class has a function called GetGameInstance() similar to GetWorld() as of 4.4 !

So this means you have global access to persistent values in your custom game instance class, in your entire code base!

void ASolusPC::PlayerTick(float DeltaTime)
 {
         Super::PlayerTick(DeltaTime);
         
         USolusGameInstance* SGI = Cast<USolusGameInstance>(GetGameInstance());
         **if**(SGI)
         { 
                 SGI->InterLevelPersistentValue++;
                 ClientMessage(FString::FromInt(SGI->InterLevelPersistentValue));
         }
         
 }

Config Setting

Make sure to set your DefaultEngine.ini to use your custom game instance!

[/Script/EngineSettings.GameMapsSettings]
 GameInstanceClass=/Script/Solus.SolusGameInstance

Other Solus C++ Tutorials

I have many Solus C++ tutorials here!

[Solus_C++_Tutorials](https://wiki.unrealengine.com/index.php?title=Solus_C%2B%2B_Tutorials)

 

来自 <<https://wiki.unrealengine.com/Game_Instance,_Custom_Game_Instance_For_Inter-Level_Persistent_Data_Storage>> 
