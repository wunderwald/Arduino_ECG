#=========================================================================
#Ardmob Preprocessing
#Data available at: 
#Code written by Markus R. Tünte (markus.tuente@univie.ac.at)
#Code last edited: 23.02.23
#=========================================================================
rm(list=ls())
# load packages
packages <- c("readr", "stringr", "dplyr", "RHRV", "tidyverse",
				"tidyr", "psych", "ggplot2", "cowplot", "ggpubr")

# Install packages not yet installed
installed_packages <- packages %in% rownames(installed.packages())
if (any(installed_packages == FALSE)) {
  install.packages(packages[!installed_packages])
}

# Packages loading
invisible(lapply(packages, library, character.only = TRUE))


#setwd
setwd(".../ardmob_analysis_r")
here::i_am(".../ardmob_analysis/r_scripts/main_analysis_r.r")

#========================================
#Load data
#========================================
##load in all ids and compute scores, then combine dfs
data_path <- here::here("data")
project_path <- here::here()
setwd(data_path)
filenames <- Sys.glob("*.csv")
filenames <- str_subset(filenames, "_ibi")
list_dfs <- c()
for(i in filenames) {						#import files for each participant				
	if(grepl("ardmob", i)) {						#arduino_ecg
		id <- substr(i, 1, 3)									#get id
		ard_name <- paste("ardmob", id, sep = "_")				#make name for saving
		ard_latency <- read.csv(i)								#load df
		ard_latency$ibi_num <- seq.int(nrow(ard_latency))		#make peak index
		ard_latency$time <- ard_latency$time * 1000 			#make ms
		ard_latency$ibi <- ard_latency$ibi * 1000 			#make ms
		colnames(ard_latency)[colnames(ard_latency) == "time"] = "time_ardmob"	#rename var
		colnames(ard_latency)[colnames(ard_latency) == "ibi"] = "ibis_ardmob"	#rename var
		ard_latency$id <- id									#make id var
		assign(ard_name, ard_latency)	
		list_dfs[i] <- ard_name[1]
	}
	if(grepl("hrv_ad", i)) {						#adinstruments_ecg
		id <- substr(i, 1, 3)						#get id
		adi_name <- paste("adi", id, sep = "_")		#make name for saving
		adi_latency <- read.csv(i)		
		adi_latency$ibi_num <- seq.int(nrow(adi_latency))
		adi_latency$ibis_adi_ecg <- c(NA, diff(adi_latency$peakIndex))
		colnames(adi_latency)[colnames(adi_latency) == "peakIndex"] = "time_adi_ecg"	#rename var
		adi_latency$id <- id
		assign(adi_name, adi_latency)
		list_dfs[i] <- adi_name[1]
	}
		if(grepl("fro", i)) {						#fro
		id <- substr(i, 1, 3)						#get id
		fro_name <- paste("fro", id, sep = "_")		#make name for saving
		fro_latency <- read.csv(i)		
		fro_latency$ibi_num <- seq.int(nrow(fro_latency))
		fro_latency$time <- fro_latency$time * 1000 			#make ms
		fro_latency$ibi <- fro_latency$ibi * 1000 			#make ms
		colnames(fro_latency)[colnames(fro_latency) == "time"] = "time_adi_fro"	#rename var
		colnames(fro_latency)[colnames(fro_latency) == "ibi"] = "ibis_adi_fro"	#rename var
		fro_latency$id <- id
		assign(fro_name, fro_latency)
		list_dfs[i] <- fro_name[1]
	}
		if(grepl("fs", i)) {						#fs
		id <- substr(i, 1, 3)						#get id
		fs_name <- paste("fs", id, sep = "_")		#make name for saving
		fs_latency <- read.csv(i)		
		fs_latency$ibi_num <- seq.int(nrow(fs_latency))
		fs_latency$ibis_fs_ecg <- c(NA, diff(fs_latency$peakIndex))
		colnames(fs_latency)[colnames(fs_latency) == "peakIndex"] = "time_adi_fs"	#rename var
		fs_latency$id <- id
		assign(fs_name, fs_latency)
		list_dfs[i] <- fs_name[1]
	}
}
setwd(project_path)
#compute difference score and make combined df	
#id1
combined_df_1 <- list(ardmob_001, fro_001, adi_001, fs_001) %>% reduce(full_join, by = "ibi_num")
#id2
combined_df_2 <- list(ardmob_002, fro_002, adi_002, fs_002) %>% reduce(full_join, by = "ibi_num")
#id3
combined_df_3 <- list(ardmob_003, fro_003, adi_003, fs_003) %>% reduce(full_join, by = "ibi_num")
#id4
combined_df_4 <- list(ardmob_004, fro_004, adi_004, fs_004) %>% reduce(full_join, by = "ibi_num")
#combine all
combined_df <- do.call("rbind", list(combined_df_1, combined_df_2, combined_df_3, combined_df_4))
head(combined_df)
write.csv(combined_df, here::here("data", "combined_df.csv"))
