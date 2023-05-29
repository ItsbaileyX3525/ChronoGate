async def LoadModel(model): #Smoothly loads models
    model=await loader.loadModel(model, blocking=False)
    return model
async def LoadAudio(path): #Smoothly loads audio files
    audioname = loader.loadSfx(path)
    return audioname
