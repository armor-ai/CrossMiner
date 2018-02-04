# CrossMiner
Release code for our ISSRE'16 paper: Experience Report: Understanding Cross-Platform App Issues from User Reviews. http://ieeexplore.ieee.org/document/7774515/
The highlight is the method which can accurately find similar words to one topic based on word embeddings and k-clustering. We mainly run experiments related to seven topics/issue types: `battery`, `crash`, `memory`, `network`, `privacy`, `spam`, and `UI`.

We automatically detect the proportion of user feedback of each issue type, and prioritize them accordingly.

## Input
An example input is given in the folder `Input`. The three folders correspond to three platforms, i.e., Google Play, App Store, and Winphone Store.

## Usage
You can run the code directly by:
```
$ python reviewsAnalyzeAll.py
```

## Discovered Topical Words of Each Issue

Issue | Keywords
---- | ---
Battery | battery, drain, usage, consumption, overheat, drainer, consume, power, hog, electricity, drainage, charger, batter, standby, discharge, energy
Crash |  crash, freeze, foreclose, lag, crush, stall, close, shut, laggy, glitch, hang, load, stuck, startup, buffer, open, laggs, freez, glitchy, buggy
Memory | memory, storage, space, gb, internal, gigabyte, ram, 6gb, occupy, 4gb, mb, 300mb, 8gb, 500mb, 16gb, byte, 5gb, gig, 2gb, 1gb, 1g
Network | network, connectivity, internet, consumption, wifi, connection, reception, conection, connect, signal, 4g, wi, 3g, broadband, fibre, lte, reconnecting, fi, wireless, reconnect, disconnect
Privacy | privacy, security, invade, safety, personal, policy, invasion, breach, protection, protect, private, disclosure, secure, unsafe, insecure, permission, fingerprint, encryption, violation, encrypt
Spam | spam, spammer, scammer, unsolicited, harassment, unwanted, bot, bombard, junk, scam, advertisement, popups, scraper, hacker
UI | ui, interface, design, layout, gui, ux, clunky, redesign, aesthetic, navigation, usability, desing, sleek, appearance, aesthetically, intuitive, minimalistic, ugly, slick, graphic, unintuitive

## Result Explanation
The proportions of each issue among user reviews are saved in `Output/Analyze_results`. The first line is the total statistics, and the last three lines correspond to the statistics of three platforms.

`example******89205******38042******0.42646******114******0.003******72******0.00189******0.63158******3.44251******2.25439******0.34513******1.375******0.60058******0.39008`
indicate:
`app_name******total_raw_review_num******total_clean_review_num******clean_raw_ratio******keywords_review_num******keywords_clean_ratio******clean_low_rating_num******low_clean_ratio******low_keywords_ratio******avg_clean_rating******avg_keywords_rating******decrease_rating_ratio_keywords_clean******decrease_rating_ratio_lowrating_clean************decrease_rating_ratio_keywords_lowrating`
