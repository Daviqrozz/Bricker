document.addEventListener('DOMContentLoaded', function () {

    // Fast sell modal
    const modalElement = document.getElementById('fastSellModal');
    if (!modalElement) return;

    const fastSellModal = new bootstrap.Modal(modalElement);
    const form = document.getElementById('fastSellForm');
    const productNameEl = document.getElementById('fastSellProductName');
    const expectedValueEl = document.getElementById('fastSellExpectedValue');
    const priceInputEl = document.getElementById('fastSellPrice');
    const errorEl = document.getElementById('fastSellError');

    document.querySelectorAll('.open-fast-sell').forEach((button) => {
      button.addEventListener('click', function () {
        const productName = this.dataset.productName;
        const expectedPrice = this.dataset.price;
        const sellUrl = this.dataset.url;

        productNameEl.textContent = productName;
        expectedValueEl.textContent = expectedPrice;
        priceInputEl.value = expectedPrice;
        errorEl.textContent = '';

        form.setAttribute('action', sellUrl);

        fastSellModal.show();
      });
    });

    form.addEventListener('submit', async function (event) {
      event.preventDefault();

      errorEl.textContent = '';

      const formData = new FormData(form);

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          credentials: 'same-origin'
        });

        const data = await response.json();

        if (response.ok && data.success) {
          fastSellModal.hide();
          window.location.reload();
        } else {
          if (data.errors && data.errors.price_sold) {
            errorEl.textContent = data.errors.price_sold.join(' ');
          } else if (data.message) {
            errorEl.textContent = data.message;
          } else {
            errorEl.textContent = 'Não foi possível concluir a venda.';
          }
        }
      } catch (error) {
        errorEl.textContent = 'Erro inesperado ao processar a venda.';
      }
    });
  });