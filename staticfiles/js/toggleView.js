// View Toggle Functionality
  document.addEventListener('DOMContentLoaded', function () {
    const tableView = document.getElementById('table-view');
    const cardsView = document.getElementById('cards-view');
    const tableBtn = document.getElementById('view-table-btn');
    const cardsBtn = document.getElementById('view-cards-btn');
    const perPageSelect = document.getElementById('per-page-select');

    // Handle per-page selector change
    if (perPageSelect) {
      perPageSelect.addEventListener('change', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('per_page', this.value);
        urlParams.set('page', '1'); // Reset to first page when changing per_page
        window.location.search = urlParams.toString();
      });
    }

    // Handle period selector change
    const periodSelect = document.getElementById('period-select');
    if (periodSelect) {
      periodSelect.addEventListener('change', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('period', this.value);
        window.location.search = urlParams.toString();
      });
    }

    // Check if we're on mobile
    const isMobile = window.innerWidth < 768;

    if (!isMobile) {
      // Desktop: Handle toggle
      const savedView = localStorage.getItem('productView') || 'table';

      function showTableView() {
        tableView.style.display = 'block';
        cardsView.style.display = 'none';
        tableBtn.classList.add('active');
        cardsBtn.classList.remove('active');
        localStorage.setItem('productView', 'table');
      }

      function showCardsView() {
        tableView.style.display = 'none';
        cardsView.style.display = 'block';
        tableBtn.classList.remove('active');
        cardsBtn.classList.add('active');
        localStorage.setItem('productView', 'cards');
      }

      // Set initial view
      if (savedView === 'cards') {
        showCardsView();
      } else {
        showTableView();
      }

      // Button click handlers
      tableBtn.addEventListener('click', showTableView);
      cardsBtn.addEventListener('click', showCardsView);
    } else {
      // Mobile: Always show cards
      tableView.style.display = 'none';
      cardsView.style.display = 'block';
    }

    // Handle window resize
    window.addEventListener('resize', function () {
      const nowMobile = window.innerWidth < 768;

      if (nowMobile) {
        tableView.style.display = 'none';
        cardsView.style.display = 'block';
      } else {
        // Restore saved preference on desktop
        const savedView = localStorage.getItem('productView') || 'table';

        if (savedView === 'cards') {
          tableView.style.display = 'none';
          cardsView.style.display = 'block';
          cardsBtn.classList.add('active');
          tableBtn.classList.remove('active');
        } else {
          tableView.style.display = 'block';
          cardsView.style.display = 'none';
          tableBtn.classList.add('active');
          cardsBtn.classList.remove('active');
        }
      }
    });
  });
