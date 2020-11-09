# CR95HF
Python class for testing cr95hd nfc modul
## Sources
### Datasheet
https://www.st.com/resource/en/datasheet/cr95hf.pdf  
### Helpful articles and other datasheets
- Cards summary
https://xionghuilin.com/iso-iec-14443-type-ab-summary/  
- UID descriptions
https://www.nxp.com/docs/en/application-note/AN10927.pdf  
- Commands described in detail!!!
http://sweet.ua.pt/andre.zuquete/Aulas/IRFID/11-12/docs/ISO-IEC_14443-3.pdf
## Calcs file
Contains claculations for nfcm impedance matching
## Notes
Using generator and osciloscope the values C1 = 57pF and C2 = 220 pF were choosed  
Yélo card is not a 14443-B Card, it's a Calypso card and uses a B' Prime Innovatron Protocol  
B' Prime cannot be recieved with CR95HF
