async function fetchInfo(){
  const url = document.getElementById('url').value.trim()
  if(!url) return alert('Link paste karo pehle!')

  document.getElementById('loader').classList.remove('hidden')
  document.getElementById('resultSection').classList.add('hidden')

  try{
    const res = await fetch('/api/info', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({url})
    })
    const data = await res.json()
    if(data.error) throw new Error(data.error)

    document.getElementById('thumb').src = data.thumbnail
    document.getElementById('title').innerText = data.title
    document.getElementById('platform').innerText = data.platform
    document.getElementById('duration').innerText = data.duration

    document.getElementById('videoList').innerHTML = data.video.map(f=>`
      <div class="item"><span>📺 ${f.quality} • ${f.ext.toUpperCase()} • ${f.size}</span><a href="${f.url}" target="_blank">Download</a></div>
    `).join('')

    document.getElementById('audioList').innerHTML = data.audio.map(f=>`
      <div class="item"><span>🎵 ${f.quality} • ${f.ext.toUpperCase()} • ${f.size}</span><a href="${f.url}" target="_blank">Download MP3</a></div>
    `).join('')

    document.getElementById('resultSection').classList.remove('hidden')
  }catch(e){
    alert(e.message)
  }finally{
    document.getElementById('loader').classList.add('hidden')
  }
}

function switchTab(type){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'))
  if(type==='video'){
    document.querySelectorAll('.tab')[0].classList.add('active')
    document.getElementById('videoList').classList.remove('hidden')
    document.getElementById('audioList').classList.add('hidden')
  }else{
    document.querySelectorAll('.tab')[1].classList.add('active')
    document.getElementById('audioList').classList.remove('hidden')
    document.getElementById('videoList').classList.add('hidden')
  }
}
