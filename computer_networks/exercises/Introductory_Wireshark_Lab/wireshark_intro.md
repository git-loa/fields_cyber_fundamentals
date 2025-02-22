#### 1. Which of the following protocols are shown as appearing (i.e., are listed in the Wireshark “protocol” column) in your trace file: TCP, QUIC, HTTP, DNS, UDP, TLSv1.2?

**Answer:** The following protocols are shown as appearing
1. Without filtering: `TCP`, `TLSv1.2`, `HTTP`, `DNS` and `UDP`
2. With filtering using `http`: `HTTP` only.
    
#### 2. How long did it take from when the HTTP GET message was sent until the HTTP OK reply was received?
**Answer:** The time it takes from when the HTTP GET message was sent until the HTTP OK reply was received is 
$$18:51:18.327286070 - 18:51:18.289307233 = 0.037978837$$


#### 3. What is the Internet address of the gaia.cs.umass.edu (also known as www-net.cs.umass.edu)?  What is the Internet address of your computer?
**Answer:**
- Internet Address of `gaia.cs.umass.edu` is `128.119.245.12`
- Internet Address of of my computer is `10.0.2.15`

#### 4. Expand the information on the HTTP message in the Wireshark “Details of selected packet” window (see Figure 3 above) so you can see the fields in the HTTP GET request message. What type of Web browser issued the HTTP request? 
**Answer:** Firefox


#### 5. Expand the information on the Transmission Control Protocol for this packet in the Wireshark “Details of selected packet” window (see Figure 3 in the lab writeup) so you can see the fields in the TCP segment carrying the HTTP message. What is the destination port number to which this HTTP request is being sent?
**Answer:** 80


#### 6. Print the two HTTP messages (GET and OK) referred to in question 2 above. To do so, select Print from the Wireshark File command menu, and select the “Selected Packet Only” and “Print as displayed” radial buttons, and then click OK.
