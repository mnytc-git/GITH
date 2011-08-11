async function getSecretHash(title) {
  const secretSalt = "MNYTC_GHOST_PROTOCOL_"; 
  const data = new TextEncoder().encode(secretSalt + title);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex.substring(0, 10);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname.endsWith('.mp4')) {
      const fileName = url.pathname.split('/').pop();
      const decodedFileName = decodeURIComponent(fileName);
      const cleanTitle = decodedFileName.replace('.mp4', '');

      const bucketCode = await getSecretHash(cleanTitle);
      
      const archiveLink = `https://archive.org/download/${bucketCode}/${bucketCode}.mp4`;

      const response = await fetch(archiveLink, {
        method: request.method,
        headers: request.headers,
        cf: {
          cacheEverything: true,
          cacheTtlByStatus: { "200-299": 2592000, "400-599": 0 }
        },
        redirect: 'follow'
      });

      if (!response.ok && response.status !== 206) {
        return env.ASSETS.fetch(request);
      }

      return response;
    }

    return env.ASSETS.fetch(request);
  }
};
