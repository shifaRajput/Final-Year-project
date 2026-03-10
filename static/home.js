// navigation bar 
const navItems = document.querySelectorAll(".navbar-center li");

navItems.forEach(item => {
  item.addEventListener("click", () => {
    navItems.forEach(i => i.classList.remove("active"));
    item.classList.add("active");
  });
});

// image slider
let curPage = 1;
const pages = document.querySelectorAll(".skw-page");
const numOfPages = pages.length;
const animTime = 1000;
let scrolling = false;
const autoSlideTime = 3000; // 3 seconds

function pagination() {
  scrolling = true;

  pages.forEach((page, index) => {
    const pageNum = index + 1;
    page.classList.remove("active", "inactive");

    if (pageNum === curPage) {
      page.classList.add("active");
      page.classList.remove("inactive");
    } else if (pageNum === curPage - 1) {
      page.classList.add("inactive");
    }
  });

  setTimeout(() => {
    scrolling = false;
  }, animTime);
}

function navigateUp() {
  if (curPage === 1) return;
  curPage--;
  pagination();
}

function navigateDown() {
  if (curPage === numOfPages) {
    curPage = 1; // loop back to first slide
  } else {
    curPage++;
  }
  pagination();
}

// Auto slide
setInterval(() => {
  if (!scrolling) {
    navigateDown();
  }
}, autoSlideTime);

document.addEventListener("click", function (e) {
  if (e.target.closest("a, button")) {
    e.stopPropagation(); // allow link navigation
  }
});

document.addEventListener("keydown", function (e) {
  if (scrolling) return;
  if (e.key === "ArrowUp") {
    navigateUp(); 
  } else if (e.key === "ArrowDown") {
    navigateDown();
  }
});

// Heart Icon
    document.addEventListener('click', (e) => {
        if(e.target.classList.contains('heart-icon')) {
            e.target.classList.toggle('fas');
            e.target.classList.toggle('far');
            e.target.classList.toggle('active');
        }
    });

    // Slider
    const sliders = document.querySelectorAll('.slider-container');
    sliders.forEach(slider => {
        let isDown = false;
        let startX;
        let scrollLeft;
        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });
        slider.addEventListener('mouseleave', () => isDown = false);
        slider.addEventListener('mouseup', () => isDown = false);
        slider.addEventListener('mousemove', (e) => {
            if(!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 2;
            slider.scrollLeft = scrollLeft - walk;
        });
    });

    // Add to Cart Animation
    document.querySelectorAll('.button').forEach(button => {
      button.addEventListener('click', e => {
          if (!button.classList.contains('loading')) {
             button.classList.add('loading');
             setTimeout(() => button.classList.remove('loading'), 3700);
           }
           e.preventDefault();
        });
    });

// chat widget
document.addEventListener("DOMContentLoaded", () => {

  const chatButton = document.getElementById("chat-button");
  const chatBox = document.getElementById("chat-box");
  const chatClose = document.getElementById("chat-close");
  const sendBtn = document.getElementById("send-btn");
  const chatText = document.getElementById("chat-text");
  const chatMessages = document.getElementById("chat-messages");

  chatButton.onclick = () => {
    chatBox.style.display = "flex";
    chatButton.style.display = "none";
  };

  chatClose.onclick = () => {
    chatBox.style.display = "none";
    chatButton.style.display = "flex";
  };

  sendBtn.onclick = sendMessage;
  chatText.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const text = chatText.value.trim();
    if (!text) return;

    const userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.textContent = text;
    chatMessages.appendChild(userMsg);

    chatText.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;

    setTimeout(() => {
      const botMsg = document.createElement("div");
      botMsg.className = "message bot";
      botMsg.textContent = "Thanks! Our team will get back to you shortly.";
      chatMessages.appendChild(botMsg);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 700);
  }

});
<script>
  const input = document.getElementById('searchInput');
  const resultsBox = document.getElementById('searchResults');
  let debounceTimer;

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const query = input.value.trim();

    if (!query) {
      resultsBox.style.display = 'none';
      return;
    }

    debounceTimer = setTimeout(async () => {
      const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
      const products = await res.json();

      if (products.length === 0) {
        resultsBox.innerHTML = '<div style="padding:12px; color:#888;">No results found</div>';
      } else {
        resultsBox.innerHTML = products.map(p => `
          <a href="/product/${p.id}" style="
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            text-decoration: none;
            color: #333;
            border-bottom: 1px solid #f0f0f0;
          " onmouseover="this.style.background='#f9f9f9'" onmouseout="this.style.background='white'">
            ${p.image
              ? `<img src="/static/uploads/${p.image}" style="width:40px;height:40px;object-fit:cover;border-radius:6px;">`
              : `<div style="width:40px;height:40px;background:#eee;border-radius:6px;"></div>`
            }
            <div>
              <div style="font-weight:600;">${p.name}</div>
              <div style="font-size:12px;color:#888;">${p.brand} · ${p.device_type} · $${p.real_price}</div>
            </div>
          </a>
        `).join('');
      }

      resultsBox.style.display = 'block';
    }, 300); // 300ms debounce
  });

  // Hide results when clicking outside
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !resultsBox.contains(e.target)) {
      resultsBox.style.display = 'none';
    }
  });

