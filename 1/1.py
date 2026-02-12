import csv

from icmplib import ping


domains = ["google.com", "yandex.ru", "youtube.com", "spotify.com", "dns.ru", 
            "github.com", "vk.com", "yahoo.com", "mail.ru", "facebook.com"]

results = [["domain", "ip", "packets_sent", "packets_received", 
            "packets_lost", "rtt(ms)"]]

for domain in domains:

    response = ping(domain, count=1)
    results.append([domain, response.address, response.packets_sent, 
                    response.packets_received, response.packet_loss, response.avg_rtt])

with open('results.csv','w', newline='') as file:

    writer = csv.writer(file)
    writer.writerow(results[0])
    writer.writerows(results[1:])
