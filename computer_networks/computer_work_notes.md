# Notes

## Proxy Server
A *proxy server* acts as an intermediary between your device and the internet. Think of it as a middleman that processes your requests to access websites, fetches the data, and then passes it back to you. Here's a rundown of its primary functions:

- **Privacy and Anonymity:** When you use a proxy server, your IP address is hidden. Websites see the IP address of the proxy server instead of yours.

- **Access Control:** Organizations often use proxy servers to control employee internet usage. It can block certain websites and log user activity.

- **Performance Improvement:** Proxy servers can cache frequently accessed websites, making it faster for you to retrieve that data.

- **Access to Restricted Content:** Proxies can help you bypass geo-restrictions and access content that might be unavailable in your region.

In essence, it helps enhance your privacy, security, and internet experience!


## Handle GET request
1. File is in cache. 
   - open it 
   - serve it to the cliet.
   - move to end of cache.
2. File not in cache.
   - fetch from web. 






## Least Recently Used.
**LRU** stands for **Least Recently Used**. It's a common caching algorithm used to manage the cache space efficiently. The key idea behind LRU is to ensure that the least recently accessed items are removed first when the cache reaches its capacity. This helps keep the most frequently or recently accessed data in the cache, improving performance.

Here's how LRU works:

1. **Access Order**: The cache maintains the access order of the items. When an item is accessed, it's moved to the most recent position.
2. **Eviction Policy**: When the cache is full, the least recently used item (the one at the end of the access order) is removed to make space for the new item.
3. **Insertion**: The new item is inserted at the most recent position in the cache.

In the context of our proxy server, LRU ensures that the cached web pages or resources are the ones that are accessed more frequently, improving the server's response time for those requests.



