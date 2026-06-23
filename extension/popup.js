const resumeInput = document.getElementById('resumeInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const statusMessage = document.getElementById('statusMessage');

chrome.storage.local.get(['savedResume'], (res) => {
  if (res.savedResume) resumeInput.value = res.savedResume;
});

analyzeBtn.addEventListener('click', async () => {
  const resumeText = resumeInput.value.trim();
  if (!resumeText) {
    statusMessage.textContent = "⚠️ Please paste your resume first.";
    return;
  }
  
  chrome.storage.local.set({ savedResume: resumeText });
  statusMessage.textContent = "🔍 Scraping active tab data...";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) {
    statusMessage.textContent = "❌ No active tab found.";
    return;
  }

  chrome.tabs.sendMessage(tab.id, { action: "scrapeJob" }, async (response) => {
    if (!response || !response.jobText) {
      statusMessage.textContent = "❌ Failed to extract job post text.";
      return;
    }

    statusMessage.textContent = "🤖 Processing through NLP Pipeline...";

    try {
      const apiRes = await fetch('http://127.0.0.1:8000/match-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: response.jobText
        })
      });

      const data = await apiRes.json();
      
      document.getElementById('matchScore').textContent = `${data.match_score}%`;
      document.getElementById('roleBadge').textContent = data.role_detected;
      
      const missingContainer = document.getElementById('missingSkills');
      missingContainer.innerHTML = '';
      data.missing_skills.forEach(skill => {
        const span = document.createElement('span');
        span.className = 'tag';
        span.textContent = skill;
        missingContainer.appendChild(span);
      });

      const recContainer = document.getElementById('recommendations');
      recContainer.innerHTML = '';
      data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recContainer.appendChild(li);
      });

      resultsSection.classList.remove('hidden');
      statusMessage.textContent = "";

    } catch (err) {
      statusMessage.textContent = "❌ Backend server down. Run uvicorn!";
      console.error(err);
    }
  });
});
