async function loadNews() {
  try {
    const response = await fetch('../daily/latest.json');
    if (!response.ok) throw new Error('daily index not found');
    const data = await response.json();
    const container = document.getElementById('news');
    if (Array.isArray(data.news)) {
      data.news.forEach(id => {
        const item = document.createElement('div');
        const link = document.createElement('a');
        link.href = `../news/${id}.json`;
        link.textContent = id;
        item.appendChild(link);
        container.appendChild(item);
      });
    } else {
      container.textContent = 'Brak danych';
    }
  } catch (err) {
    document.getElementById('news').textContent = err.message;
  }
}

loadNews();
