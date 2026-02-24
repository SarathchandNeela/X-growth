const STORAGE_KEY = "dealguys-custom-deals";
const THEME_KEY = "dealguys-theme";

const seedDeals = [
  {
    id: "d1",
    title: "Boat Airdopes 131 at 72% Off",
    store: "Amazon",
    url: "https://www.amazon.in/",
    coupon: "BOAT72",
    category: "electronics",
    description: "Limited-time earbud deal with free delivery and no-cost EMI.",
    tags: ["audio", "bestseller", "limited"],
    posted: "2h ago",
  },
  {
    id: "d2",
    title: "Buy 1 Get 1 Pizza Thursday",
    store: "Domino's",
    url: "https://www.dominos.co.in/",
    coupon: "PIZZABOGO",
    category: "food",
    description: "Apply code at checkout to unlock buy-one-get-one offer.",
    tags: ["food", "bogo"],
    posted: "4h ago",
  },
  {
    id: "d3",
    title: "Flat ₹150 Off on First Flight Booking",
    store: "MakeMyTrip",
    url: "https://www.makemytrip.com/",
    coupon: "FIRSTFLY",
    category: "travel",
    description: "New users can claim instant discount on domestic routes.",
    tags: ["travel", "new-user"],
    posted: "6h ago",
  },
];

const form = document.querySelector("#deal-form");
const searchInput = document.querySelector("#search-input");
const feed = document.querySelector("#deal-feed");
const empty = document.querySelector("#empty-state");
const template = document.querySelector("#deal-template");
const filters = document.querySelector("#category-filters");
const themeToggle = document.querySelector("#theme-toggle");
const storesEl = document.querySelector("#popular-stores");

let currentCategory = "all";
let deals = loadDeals();

initTheme();
renderDeals();
renderStores();

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const data = new FormData(form);
  deals.unshift({
    id: crypto.randomUUID(),
    title: data.get("title").toString().trim(),
    store: data.get("store").toString().trim(),
    url: data.get("url").toString().trim(),
    coupon: data.get("coupon").toString().trim() || "NO CODE",
    category: data.get("category").toString().trim(),
    description: data.get("description").toString().trim(),
    tags: [data.get("category").toString().trim(), "community"],
    posted: "just now",
  });
  persistDeals();
  renderDeals();
  renderStores();
  form.reset();
});

searchInput.addEventListener("input", renderDeals);

filters.addEventListener("click", (e) => {
  const button = e.target.closest("button[data-category]");
  if (!button) return;
  currentCategory = button.dataset.category;
  document.querySelectorAll("#category-filters .chip").forEach((chip) => {
    chip.classList.toggle("active", chip === button);
  });
  renderDeals();
});

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  const dark = document.body.classList.contains("dark");
  localStorage.setItem(THEME_KEY, dark ? "dark" : "light");
  themeToggle.textContent = dark ? "☀️" : "🌙";
});

function renderDeals() {
  const query = searchInput.value.trim().toLowerCase();
  feed.innerHTML = "";

  const filtered = deals.filter((deal) => {
    const categoryOk = currentCategory === "all" || deal.category === currentCategory;
    const queryOk = !query || `${deal.title} ${deal.store} ${deal.tags.join(" ")}`.toLowerCase().includes(query);
    return categoryOk && queryOk;
  });

  empty.style.display = filtered.length ? "none" : "block";

  filtered.forEach((deal) => {
    const node = template.content.cloneNode(true);
    node.querySelector(".meta").textContent = `${deal.store} • ${deal.posted}`;
    node.querySelector("h3").textContent = deal.title;
    node.querySelector(".badge").textContent = deal.category;
    node.querySelector(".description").textContent = deal.description;
    node.querySelector(".coupon").textContent = deal.coupon;

    const tagsEl = node.querySelector(".tags");
    deal.tags.forEach((tag) => {
      const span = document.createElement("span");
      span.className = "tag";
      span.textContent = `#${tag}`;
      tagsEl.appendChild(span);
    });

    const cta = node.querySelector(".cta");
    cta.href = deal.url;

    node.querySelector(".delete").addEventListener("click", () => {
      deals = deals.filter((d) => d.id !== deal.id);
      persistDeals();
      renderDeals();
      renderStores();
    });

    feed.appendChild(node);
  });
}

function renderStores() {
  const counts = deals.reduce((acc, deal) => {
    acc[deal.store] = (acc[deal.store] || 0) + 1;
    return acc;
  }, {});
  const top = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6);

  storesEl.innerHTML = "";
  top.forEach(([store, count]) => {
    const li = document.createElement("li");
    li.textContent = `${store} (${count})`;
    storesEl.appendChild(li);
  });
}

function loadDeals() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [...seedDeals];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.length ? parsed : [...seedDeals];
  } catch {
    return [...seedDeals];
  }
}

function persistDeals() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(deals));
}

function initTheme() {
  const mode = localStorage.getItem(THEME_KEY);
  if (mode === "dark") {
    document.body.classList.add("dark");
    themeToggle.textContent = "☀️";
  }
}
