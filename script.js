function baixar() {
  const url = document.getElementById('url').value;
  const tipo = document.getElementById('tipo').value;

  fetch('/baixar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, tipo })
  })
  .then(res => res.blob())
  .then(blob => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `youtube_${tipo}.` + (tipo === 'audio' ? 'mp3' : 'mp4');
    link.click();
  });
}
