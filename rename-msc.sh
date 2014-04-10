#!/bin/bash
# rename-msc.sh: Rename mp3 files of MILESTONE SOUND COLLECTION.

MSC_ROOT='D:/data'
RENAME=mv

# D:/data/MSC-01:
declare -A MSC1=( \
    ["01 トラック 1.mp3"]="1_01_kairo -chaosfield image-" \
    ["02 トラック 2.mp3"]="1_02_in to the machine -opening demo-" \
    ["03 トラック 3.mp3"]="1_03_25mg select" \
    ["04 トラック 4.mp3"]="1_04_change the phase -exposition-" \
    ["05 トラック 5.mp3"]="1_05_not back to time -phase 1-" \
    ["06 トラック 6.mp3"]="1_06_coccus -phase 2-" \
    ["07 トラック 7.mp3"]="1_07_human's figure -phase 3-" \
    ["08 トラック 8.mp3"]="1_08_spray -boss-" \
    ["09 トラック 9.mp3"]="1_09_spinout -phase 4-" \
    ["10 トラック 10.mp3"]="1_10_back in to the machine -phase 5-" \
    ["11 トラック 11.mp3"]="1_11_despair -last boss-" \
    ["12 トラック 12.mp3"]="1_12_contact lost -end roll-" \
    ["13 トラック 13.mp3"]="1_13_radio allergy -Advertise Demo-" \
    ["14 トラック 14.mp3"]="1_14_bitcrush -Character Select-" \
    ["15 トラック 15.mp3"]="1_15_chatterbox -Tutorial-" \
    ["16 トラック 16.mp3"]="1_16_ukiha shopping mall -Stage 01-" \
    ["17 トラック 17.mp3"]="1_17_a day in the park -Stage 02-" \
    ["18 トラック 18.mp3"]="1_18_2 the Sky -Stage 03-" \
    ["19 トラック 19.mp3"]="1_19_the ordinary people -Stage Boss-" \
    ["20 トラック 20.mp3"]="1_20_i hate tha sun -Stage 04-" \
    ["21 トラック 21.mp3"]="1_21_24_7 -Stage 05-" \
    ["22 トラック 22.mp3"]="1_22_FINALE -Last Boss-" \
    ["23 トラック 23.mp3"]="1_23_asagiri -Final Boss-" \
    ["24 トラック 24.mp3"]="1_24_Illegal Function -Ending Demo-" \
    ["25 トラック 25.mp3"]="1_25_Skip & Roll -Ranking-" \
)

# D:/data/MSC-02:
declare -A MSC2=( \
    ["01 トラック 1.mp3"]="2_01_sky was blue, sky was blue... -Advertise Demo-" \
    ["02 トラック 2.mp3"]="2_02_honeys and blue -Mode Select-" \
    ["03 トラック 3.mp3"]="2_03_Atheistic Love -Tutorial-" \
    ["04 トラック 4.mp3"]="2_04_1000 clouds -Stage1-" \
    ["05 トラック 5.mp3"]="2_05_one thing reality -Stage2-" \
    ["06 トラック 6.mp3"]="2_06_you can't fxxk me -Stage3-" \
    ["07 トラック 7.mp3"]="2_07_the extraordinary people -Boss-" \
    ["08 トラック 8.mp3"]="2_08_Electric Chair -Stage4-" \
    ["09 トラック 9.mp3"]="2_09_death from above 4098 -Stage5-" \
    ["10 トラック 10.mp3"]="2_10_hey little girl, go home soon -Last Boss-" \
    ["11 トラック 11.mp3"]="2_11_Sex pervert of a silence -True Boss-" \
    ["12 トラック 12.mp3"]="2_12_honeys and blue - dub -Easy End-" \
    ["13 トラック 13.mp3"]="2_13_Lily in desert -Staff Roll-" \
    ["14 トラック 14.mp3"]="2_14_the clean rooms -Name Entry-" \
    ["15 トラック 15.mp3"]="2_15_ILLMATIC ENVELOPE -advertise demo-" \
    ["16 トラック 16.mp3"]="2_16_HERMIT NETWORK -tutorial-" \
    ["17 トラック 17.mp3"]="2_17_PHANTOM'S DANCE -stage1-" \
    ["18 トラック 18.mp3"]="2_18_MAGURO -stage2-" \
    ["19 トラック 19.mp3"]="2_19_ROOFIE -stage3-" \
    ["20 トラック 20.mp3"]="2_20_PIZZA PHAT ILLER -boss-" \
    ["21 トラック 21.mp3"]="2_21_I WANNA BE WITH YOU IN THIS WORLD -stage4-" \
    ["22 トラック 22.mp3"]="2_22_Mr. RADIO SHOCK -stage5-" \
    ["23 トラック 23.mp3"]="2_23_CHANNEL FANNEL -last boss-" \
    ["24 トラック 24.mp3"]="2_24_KILLER TUNE STORE -true boss-" \
    ["25 トラック 25.mp3"]="2_25_CONVERGENCE -ending-" \
    ["26 トラック 26.mp3"]="2_26_NOSTALGIA -staffroll-" \
    ["27 トラック 27.mp3"]="2_27_SANCTUARY -name entry-" \
    ["28 トラック 28.mp3"]="2_28_ROOFIE -showerheadz remix-" \
    ["29 トラック 29.mp3"]="2_29_KILLER TUNE STORE -showerheadz remix-" \
)

# D:/data/MSC-03:
declare -A MSC3=( \
    ["01 トラック 1.mp3"]="3_01_Good-bye" \
    ["02 トラック 2.mp3"]="3_02_Pandora" \
    ["03 トラック 3.mp3"]="3_03_Psychopath" \
    ["04 トラック 4.mp3"]="3_04_Talk To The Wind" \
    ["05 トラック 5.mp3"]="3_05_The method of setting the password" \
    ["06 トラック 6.mp3"]="3_06_Tokyo Eight Spots" \
    ["07 トラック 7.mp3"]="3_07_The Ordinaly People [shaped]" \
    ["08 トラック 8.mp3"]="3_08_I'm boring" \
    ["09 トラック 9.mp3"]="3_09_Pill Case" \
    ["10 トラック 10.mp3"]="3_10_5 Questions" \
    ["11 トラック 11.mp3"]="3_11_Blue Flower" \
    ["12 トラック 12.mp3"]="3_12_Keep Quipu" \
    ["13 トラック 13.mp3"]="3_13_The Setting Sun" \
    ["14 トラック 14.mp3"]="3_14_Humanlost Funk" \
    ["15 トラック 15.mp3"]="3_15_The Tongue Of The Woman" \
    ["16 トラック 16.mp3"]="3_16_Liver Dysfunction" \
    ["17 トラック 17.mp3"]="3_17_Stack" \
    ["18 トラック 18.mp3"]="3_18_Mail Practice -menu-" \
    ["19 トラック 19.mp3"]="3_19_Nairobi -gallery mode-" \
    ["20 トラック 20.mp3"]="3_20_Minus Love -massive mode-" \
    ["21 トラック 21.mp3"]="3_21_the ordinaly people dub -massive mode boss-" \
    ["22 トラック 22.mp3"]="3_22_human's wild figure -death mode-" \
)

# D:/data/MSC-04:
declare -A MSC4=( \
    ["01 トラック 1.mp3"]="4_01_crazy cherry -menu-" \
    ["02 トラック 2.mp3"]="4_02_not back to time (remix) -phase 1-" \
    ["03 トラック 3.mp3"]="4_03_coccus (remix) -phase 2-" \
    ["04 トラック 4.mp3"]="4_04_human's figure (remix) -phase 3-" \
    ["05 トラック 5.mp3"]="4_05_spinout (remix) -phase 4-" \
    ["06 トラック 6.mp3"]="4_06_back in to the machine (remix) -phase 5-" \
    ["07 トラック 7.mp3"]="4_07_contact lost (edit) -end roll-" \
    ["08 トラック 8.mp3"]="4_08_coccus (umbra remix)" \
    ["09 トラック 9.mp3"]="4_09_not back to time (9090909 remix)" \
    ["10 トラック 10.mp3"]="4_10_kairo (CFL Room738)" \
    ["11 トラック 11.mp3"]="4_11_25mg (dub)" \
    ["12 トラック 12.mp3"]="4_12_1000 Clouds (extend edit)" \
    ["13 トラック 13.mp3"]="4_13_you can't fxxk me (extend edit)" \
    ["14 トラック 14.mp3"]="4_14_Atheistic Love (extend dub)" \
    ["15 トラック 15.mp3"]="4_15_ukiha shopping mall (dubstem exp.)" \
    ["16 トラック 16.mp3"]="4_16_24_7 (extend edit)" \
    ["17 トラック 17.mp3"]="4_17_Mr. RADIO SHOCK (extend edit)" \
    ["18 トラック 18.mp3"]="4_18_I Wanna Be With You In This World (fxxked)" \
    ["19 トラック 19.mp3"]="4_19_Sex Pervert Of Silence (dat bxxxh)" \
)

# MSC-mashima (NATSUGEYA Limited Bonus Disc)
declare -A MSCn=( \
    ["01 トラック 1.mp3"]="n_01_you can't fxxk me -intensive dub beyond-" \
    ["02 トラック 2.mp3"]="n_02_death from above 4098 -mashima dub-" \
)

#cd ${MSC_ROOT}/MSC-01
#for i in "${!MSC1[@]}" ; do
#    $RENAME "$i" "${MSC1[$i]}".mp3
#done
#
#cd ${MSC_ROOT}/MSC-02
#for i in "${!MSC2[@]}" ; do
#    $RENAME "$i" "${MSC2[$i]}".mp3
#done
#
#cd ${MSC_ROOT}/MSC-03
#for i in "${!MSC3[@]}" ; do
#    $RENAME "$i" "${MSC3[$i]}".mp3
#done
#
#cd ${MSC_ROOT}/MSC-04
#for i in "${!MSC4[@]}" ; do
#    $RENAME "$i" "${MSC4[$i]}".mp3
#done

cd ${MSC_ROOT}/MSC-mashima
for i in "${!MSCn[@]}" ; do
    $RENAME "$i" "${MSCn[$i]}".mp3
done
