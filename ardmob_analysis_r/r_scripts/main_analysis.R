#=========================================================================
#Ardmob Main Analysis
#Data available at: 
#Code written by Markus R. Tünte (markus.tuente@univie.ac.at)
#Code last edited: 24.02.23
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
here::i_am(".../ardmob_analysis_r/r_scripts/main_analysis.r")
save_plots <- "no"		#set to yes if you want to create plots
#========================================
#Load data
#========================================
combined_df <- read.csv(here::here("data", "combined_df.csv"))
head(combined_df)


#========================================
#Compute descriptive stats for IBIs
#========================================
#remove outliers, samller 700 or larger 1500 looks like artifacts
table(combined_df$ibis_adi_ecg)	
table(combined_df$ibis_ardmob)	
table(combined_df$ibis_adi_fro)	
table(combined_df$ibis_fs_ecg)	

#remove for fro and fs
combined_df$ibis_adi_fro[combined_df$ibis_adi_fro > 1500] <- NA
combined_df$ibis_fs_ecg[combined_df$ibis_fs_ecg > 1500] <- NA
combined_df$ibis_fs_ecg[combined_df$ibis_fs_ecg < 700] <- NA

#get descriptive stats
mean(combined_df$ibis_adi_ecg, na.rm = TRUE)	#944.1407
sd(combined_df$ibis_adi_ecg, na.rm = TRUE)		#103.9629
mean(combined_df$ibis_ardmob, na.rm = TRUE)		#944.145
sd(combined_df$ibis_ardmob, na.rm = TRUE)		#104.0626
mean(combined_df$ibis_adi_fro, na.rm = TRUE)	#944.6695
sd(combined_df$ibis_adi_fro, na.rm = TRUE)		#104.2623
mean(combined_df$ibis_fs_ecg, na.rm = TRUE)		#944.598
sd(combined_df$ibis_fs_ecg, na.rm = TRUE)		#105.3002
colSums(!is.na(combined_df))	#ard = 1400, adi = 1400, fro = 1389, fs = 1383

#prepare df for plot
df_ibi <- c()
df_ibi <- combined_df %>% pivot_longer(
	cols = starts_with("ibis_"),
	names_to = "Reference",
	values_to = "ibi")
head(df_ibi)


#rename
df_ibi$Reference[df_ibi$Reference == "ibis_ardmob"] <- "ArdMob"
df_ibi$Reference[df_ibi$Reference == "ibis_adi_fro"] <- "FastResponseOutput"
df_ibi$Reference[df_ibi$Reference == "ibis_adi_ecg"] <- "AdInstruments ECG"
df_ibi$Reference[df_ibi$Reference == "ibis_fs_ecg"] <- "Finger Sensor"

#make plot
df_ibi_plot <- gghistogram(df_ibi, x = "ibi", add = "mean", 
	fill = "Reference", xlab = "IBIs ms")
if(save_plots == "yes") {
	ggsave(here::here("figures", "ibi_histogram.jpg"))
}	


#make a plot only for ArdMob and AdI
#prepare df for plot
df_ard_adi <- c()
df_ard_adi <- combined_df %>% pivot_longer(
	cols = starts_with("ibis_"),
	names_to = "Reference",
	values_to = "ibi")
df_ard_adi <- subset(df_ard_adi, Reference == "ibis_adi_ecg" | Reference == "ibis_ardmob")
head(df_ard_adi)


#rename
df_ard_adi$Reference[df_ard_adi$Reference == "ibis_ardmob"] <- "ArdMob"
df_ard_adi$Reference[df_ard_adi$Reference == "ibis_adi_ecg"] <- "AdInstruments ECG"

#make plot
df_ard_adi_plot <- gghistogram(df_ard_adi, x = "ibi", add = "mean", 
	fill = "Reference", xlab = "IBIs ms")
if(save_plots == "yes") {
	ggsave(here::here("figures", "ibi_ard_adi_histogram.jpg"))
}	


#========================================
#Compare timings
#========================================
#combine dfs
combined_df_latency <- combined_df
head(combined_df_latency)
#compute latency scores with adi ecg as reference
combined_df_latency$score_ardmob <- combined_df_latency$time_ardmob - combined_df_latency$time_adi_ecg	#ardmob
combined_df_latency$score_fro <- combined_df_latency$time_adi_fro - combined_df_latency$time_adi_ecg	#fro
combined_df_latency$score_fs <- combined_df_latency$time_adi_fs - combined_df_latency$time_adi_ecg		#fs	
#set outliers to NA
table(combined_df_latency$score_ardmob)	#looks fine
table(combined_df_latency$score_fro)	#larger 200 are probably mismatched beats
table(combined_df_latency$score_fs)		#smaller 0 or larger 500 are probably mismatched beats
#how many beats?
colSums(!is.na(combined_df_latency))	#time_adi_ecg = 1404
#beats not identified before removal
sum(is.na(combined_df_latency$score_ardmob))	#1
sum(is.na(combined_df_latency$score_fro))		#9
sum(is.na(combined_df_latency$score_fs))		#2
#remove outliers
combined_df_latency$score_fro[combined_df_latency$score_fro > 200] <- NA
combined_df_latency$score_fs[combined_df_latency$score_fs > 500] <- NA
combined_df_latency$score_fs[combined_df_latency$score_fs < 0] <- NA
#beats not identified before removal
sum(is.na(combined_df_latency$score_ardmob))	#1
sum(is.na(combined_df_latency$score_fro))		#249 (240 new, so 240/1405 = 17.08%)
sum(is.na(combined_df_latency$score_fs))		#241 (239 new, so 7/1405 = 17.01%)
#descriptive stats
mean(combined_df_latency$score_ardmob, na.rm = TRUE)	#8.022792
sd(combined_df_latency$score_ardmob, na.rm = TRUE)		#5.267964
mean(combined_df_latency$score_fro, na.rm = TRUE)		#-3.513841
sd(combined_df_latency$score_fro, na.rm = TRUE)			#3.316857
mean(combined_df_latency$score_fs, na.rm = TRUE)		#281.5739
sd(combined_df_latency$score_fs, na.rm = TRUE)			#20.05758


#plot
#prepare df
df_latency_plot <- c()
df_latency_plot <- combined_df_latency %>% pivot_longer(
	cols = starts_with("score"),
	names_to = "ecg",
	values_to = "timings")
head(df_latency_plot)

#look at ardmob & fro	
df_latency_plot_ardfro <- subset(df_latency_plot, ecg == "score_ardmob" | ecg == "score_fro")
colnames(df_latency_plot_ardfro)[colnames(df_latency_plot_ardfro) == "ecg"] = "Reference"	#rename var
df_latency_plot_ardfro$Reference[df_latency_plot_ardfro$Reference == "score_ardmob"] <- "ArdMob"
df_latency_plot_ardfro$Reference[df_latency_plot_ardfro$Reference == "score_fro"] <- "FastResponseOutput"
latency_plot_ardfro <- gghistogram(df_latency_plot_ardfro, x = "timings", add = "mean", 
	fill = "Reference", xlab = "difference in ms") +
	geom_vline(xintercept = 0)
if(save_plots == "yes") {
	ggsave(here::here("figures", "latency_histogram.jpg"))
}	



#========================================
#Prepare data in RHRV for example participant and plots
#========================================	
participant <- "1"										#select participant
ard_data <- subset(combined_df, id.x == participant)		
ard_data$time_ardmob <- ard_data$time_ardmob/1000		#transform into seconds
ard_data$time_adi_ecg <- ard_data$time_adi_ecg/1000		#transform into seconds
ard_data <- ard_data[complete.cases(ard_data$time_ardmob),]

#load into RHRV
ard_hrv <- CreateHRVData() |> 
			LoadBeatVector(ard_data$time_ardmob) |>
			BuildNIHR() |>
			InterpolateNIHR()
adi_hrv <- CreateHRVData() |> 
			LoadBeatVector(ard_data$time_adi_ecg) |>
			BuildNIHR() |>
			InterpolateNIHR()


#look at Frequency Domain Analysis
ard_hrv_freq <- CreateFreqAnalysis(ard_hrv)				#ard ecg
ard_hrv_freq <- CalculatePowerBand(ard_hrv_freq, type = "wavelet")
adi_hrv_freq <- CreateFreqAnalysis(adi_hrv)				#adi ecg
adi_hrv_freq <- CalculatePowerBand(adi_hrv_freq, type = "wavelet")

#========================================
#Poincare plot & ibi histogram
#========================================
save_name <- paste("ard_fro_comparison_", participant, ".png", sep = "")
if(save_plots == "yes") {
	png(here::here("figures", save_name), units = "in", width = 11, height = 8.5, res = 300)
}	
par(mfrow=c(3,2))

##hist ibi
hist(ard_data$ibis_ardmob, xlab = "IBIs", main = "ArdMob ECG \nIBIs", 
		breaks = "FD", xlim = c(700,1400))
hist(ard_data$ibis_adi_ecg, xlab = "IBIs", main = "AdInstruments ECG \nIBIs", 
		breaks = "FD", xlim = c(700,1400))
		
##plot timeseries
PlotHR(ard_hrv, main = "Interpolated HR")
PlotHR(adi_hrv, main = "Interpolated HR")

##make poincare plot
ard_hrv_nl <- CreateNonLinearAnalysis(ard_hrv)
ard_hrv_nl <- PoincarePlot(ard_hrv_nl, doPlot = T)
adi_hrv_nl <- CreateNonLinearAnalysis(adi_hrv)
adi_hrv_nl <- PoincarePlot(adi_hrv_nl, doPlot = T)

#save plot
if(save_plots == "yes") {
	dev.off()
}

#========================================
#Look at frequency domain analysis
#========================================
#ArdMob
save_name <- paste("ardmob_frequency_domain_analysis_", participant, ".jpg", sep = "")
if(save_plots == "yes") {
	jpeg(here::here("figures", save_name))
}
ard_freq_plot <- PlotPowerBand(ard_hrv_freq, indexFreqAnalysis = 1, normalized = TRUE)
title(main = "A) ArdMob ECG", outer = TRUE, adj = 0.01, line = -1)
if(save_plots == "yes") {
	dev.off()
}


#AdIECG
save_name <- paste("adiecg_frequency_domain_analysis_", participant, ".jpg", sep = "")
if(save_plots == "yes") {
	jpeg(here::here("figures", save_name))
	}
adi_freq_plot <- PlotPowerBand(adi_hrv_freq, indexFreqAnalysis = 1, normalized = TRUE)
title(main = "B) AdInstruments ECG", outer = TRUE, adj = 0.01, line = -1)
if(save_plots == "yes") {
	dev.off()
}

