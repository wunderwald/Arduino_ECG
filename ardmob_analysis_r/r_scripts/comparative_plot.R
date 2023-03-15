#=========================================================================
#Comparative Plot
#Data available at: 
#Code written by Markus R. Tünte (markus.tuente@univie.ac.at)
#Code last edited: 28.02.23
#=========================================================================
rm(list=ls())
# load packages
packages <- c("readr", "stringr", "dplyr", "tidyverse", "here",
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

#========================================
#Load data
#========================================
xdata <- read.csv(here::here("data", "comparative_plot_data.csv"))
head(xdata)

#select random time window for vis
xdata <- subset(xdata, time < 115)
xdata <- subset(xdata, time > 100)
head(xdata)

#make time range start at 0s
xdata$time <- xdata$time - 100

#rename vars
xdata <- xdata %>% rename(
		"Time" = "time",
		"AdInstruments_ECG" = "adi_ecg",
		"Fingersensor" = "adi_finger",
		"FastResponseOutput" = "adi_fro",
		"ArdMobEKG" = "ard_fro")
head(xdata)


#make data longer for plot
xdata <- xdata %>% pivot_longer(
		cols = c("AdInstruments_ECG", "Fingersensor", "FastResponseOutput", "ArdMobEKG"),
		names_to = "ECG", values_to = "values")
head(xdata)

#make the plot
ggplot(xdata, aes(x = Time, y = values)) +
	geom_line(aes(color = ECG)) +
	scale_color_manual(values = c("#009E73", "#0072B2", "#D55E00", "#CC79A7")) +
	scale_x_continuous(limits = c(0, 15), n.breaks = 15) +
	facet_grid(ECG ~ ., scales = "free_y") +
	theme_bw() +
	theme(legend.position = "none") +
	ylab("") + xlab("Time in seconds")


#save
ggsave(here::here("figures", "compare_plot.png"), dpi = 700)
	
