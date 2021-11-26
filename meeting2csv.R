
convert2Wav <- function(fileNameMp3){
  #convert mp3 to .wav
  if(.Platform$OS.type == "windows") withAutoprint({
    memory.size()
    memory.size(TRUE)
    memory.limit()
  })
  memory.limit(size=25000)
  nameWave <- paste(substr(fileNameMp3,1,nchar(fileNameMp3)-4),".wav", sep = "")
  mp3_audio = monitoR::readMP3(fileNameMp3)
  tuneR::writeWave(mp3_audio,filename = nameWave,extensible=FALSE)
  return(name)
}

breakDownMeeting <- function(fileName, outputFolder,length){
  SECTION_LENGTH <- length
  
  #calculate how many bits the meeting will result in (num_iterations)
  
  print(outputFolder)
  setwd('removeSilence/silenced')
  #print(getwd())
  #print(strsplit(fileName, '/', fixed=T))
  #print(getwd())
  #fileName= 'ZaraL10Non-Silenced.wav'
  sound <- tuneR::readWave(fileName)
  sound_length <- round(length(sound@left) / sound@samp.rate, 2)
  
  #Check that the sound file is more than 10s
  try(if(sound_length < 10) stop("Sound file is not long enough. Should be more than 10 seconds."))
  
  num_iterations <- floor(sound_length/SECTION_LENGTH)
  #num_iterations <- 60
  
  #break down meeting in bits of size 'length'
  for (i in 0:(num_iterations-1)) {
    sectionName <- paste("section",i+101,".wav", sep = "")
    section <- tuneR::readWave(filename = fileName, from = (i*SECTION_LENGTH), to = ((i+1)*SECTION_LENGTH), unit = "seconds")
    #print(strsplit(outputFolder,'/', fixed=T))
    #outputFolder = 'ZaraL10Non-Silenced'
    setwd(outputFolder)
    tuneR::writeWave(section, filename=sectionName, extensible=FALSE)
    setwd('..')
  }
}

processAudio <- function(folderName,length) {
  # Start with empty data.frame.
  data <- data.frame()
  
  # Get list of files in the folder.
  list <- list.files(folderName, '\\.wav')
  #print(folderName)
  # Add file list to data.frame for processing.
  for (fileName in list) {
    row <- data.frame(fileName, 0, 0, length)
    data <- rbind(data, row)
  }
  # Set column names.
  names(data) <- c('sound.files', 'selec', 'start', 'end')
  
  # Move into folder for processing.
  setwd(folderName)
  
  # Process files.
  acoustics <- specan3(data, parallel=1)
  
  # Move back into parent folder.
  setwd('..')
  
  acoustics
}

meeting2csv <- function(fileNameWave){
  
  #create new name from filename by removing '.wav'
  shortName <- substr(fileNameWave,1,nchar(fileNameWave)-4)
  outputFolder <- shortName
  dir.create(outputFolder)
  folderNameSplit = unlist(strsplit(shortName, '/'))
  outputFolder = toString(folderNameSplit[length(folderNameSplit)])
  fileNameSplit = unlist(strsplit(fileNameWave, '/'))
  fileNameWave= toString(fileNameSplit[length(fileNameSplit)])
  
  breakDownMeeting(fileNameWave, outputFolder, 10)

  meeting <- processAudio(outputFolder,10)
  
  data <- rbind(meeting)
  
  # Remove unused columns.
  data$duration <- NULL
  data$sound.files <- NULL
  data$selec <- NULL
  data$peakf <- NULL
  
  # Remove rows containing NA's.
  data <- data[complete.cases(data),]
  
  nameCSV <- paste(fileNameWave, '.csv', sep="")
  
  # Write out csv dataset.
  write.csv(data, file = nameCSV, row.names=F)
  
  return(nameCSV)
}
