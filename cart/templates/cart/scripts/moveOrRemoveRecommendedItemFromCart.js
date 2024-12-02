document.querySelectorAll('.add-to-cart-form').forEach(function(form) {
    form.removeEventListener('submit', addToCartListener);
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const cartFormSubmit = async function (form) {
            const isInCart = form.dataset.isInCart === "true";
            const url = isInCart ? form.dataset.removeUrl : form.dataset.addUrl;

            form.setAttribute("action", url);

            try {
                const response = await fetch(url, {
                    method: "POST",
                    body: new FormData(form)
                });

                const data = await response.json();

                if (data.status === "success") {
                    const grandTotalElement = document.getElementById("grand-total-price");
                    const countElement = document.getElementById("total-count");
                    const taxesElement = document.getElementById("taxes");
                    const productsSubTotalPriceElement = document.getElementById('products-total-price')

                    countElement.textContent = interpolate(gettext('%s эл.'), [data.totalQuantity]);
                    grandTotalElement.textContent = data.cartGrandTotal;
                    productsSubTotalPriceElement.textContent = data.cartSubTotal;
                    taxesElement.textContent = data.taxes;

                    updateCartButtonState(form, !isInCart);
                    // showToast(data.detail, isInCart ? "danger" : "success");
                } else {
                    showToast(data.detail, "danger");
                };
            } catch (error) {
                console.error(error);
                showToast(gettext("Произошла ошибка. Повторите попытку позже."), "danger");
            };
        };

        cartFormSubmit(event.target);

        const productCard = form.closest('.card');

        const productLink = productCard.querySelector('a').href;
        const productImage = productCard.querySelector('img');
        const productImageSrc = productImage.src;
        const productImageAlt = productImage.alt;
        const productName = productCard.querySelector('.card-title').innerText;

        const productDiscountedPrice = productCard.querySelector('.product-discounted-price') ? 
                                       productCard.querySelector('.product-discounted-price').innerText : null;
        const productOldPrice = productCard.querySelector('.product-old-price') ? 
                                productCard.querySelector('.product-old-price').innerText : null;
        const productPrice = productCard.querySelector('.product-price') ? 
                             productCard.querySelector('.product-price').innerText : null;

        const productSlug = form.querySelector('input[name="product_slug"]').value;
        const productsListContainer = document.getElementById("products-list-container");
        const emptyCartImage = document.getElementById("no-image-container");
        const checkoutButton = document.getElementById("btn-checkout");

        const productIsBouquet = form.dataset.isBouquet === "true";
        const productIsInCart = form.dataset.isInCart === "true";
        const clearCartButton = document.getElementById('cart-clear-button');

        const productInfo = {
            link: productLink,
            image: productImageSrc,
            imageAlt: productImageAlt,
            name: productName,
            discountedPrice: productDiscountedPrice,
            oldPrice: productOldPrice,
            price: productPrice,
            slug: productSlug,
            isBouquet: productIsBouquet,
            isIncart: productIsInCart,
        };

        if (productInfo.isIncart) {
            const productElement = productsListContainer.querySelector(`[data-id='${productInfo.slug}']`);
            const productHr = productsListContainer.querySelector(`[data-id='${productInfo.slug}Hr']`);
            if (productElement) {
                productElement.remove()
            }
            if (productHr) {
                productHr.remove()
            }

            if (productsListContainer.children.length === 1) {
                emptyCartImage.classList.remove("d-flex");
                emptyCartImage.classList.add("d-none");
                clearCartButton.classList.add("disabled")
                checkoutButton.classList.add("disabled");
            }
            return
        }
        
        const langValue = document.documentElement.getAttribute('lang');
        const subtotal = productInfo.discountedPrice ? productInfo.discountedPrice : productInfo.price;
        const csrfToken = productCard.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const removeProductLink = productInfo.isBouquet ? `/${langValue}/cart/bouquet/remove/` : `/${langValue}/cart/product/remove/`
        const decreaseProductLink = productInfo.isBouquet ? `/${langValue}/cart/bouquet/decrease/` : `/${langValue}/cart/product/decrease/`
        const increaseProductLink = productInfo.isBouquet ? `/${langValue}/cart/bouquet/increase/` : `/${langValue}/cart/product/increase/`

        let needsHr = true;
        if (productsListContainer.children.length === 1) {
            needsHr = false;
            clearCartButton.classList.remove("disabled")
            emptyCartImage.classList.remove("d-flex");
            emptyCartImage.classList.add("d-none");
            checkoutButton.classList.remove("disabled");
        }

        const newProductElement = `
    ${needsHr ? `<hr data-id="${productInfo.slug}Hr">` : ''}
    <div class="row product-container" data-id="${productInfo.slug}">
        <div class="col-lg-3 col-md-12 mb-4 mb-lg-0">
            <div class="bg-image hover-overlay ripple image-wrapper">
                <a href="${productInfo.link}">
                    <img src="${productInfo.image}" class="square-image rounded img-thumbnail" alt="${productInfo.imageAlt}">
                </a>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 mb-4 mb-lg-0">
            <a href="${productInfo.link}" class="text-decoration-none text-dark product-name">${productInfo.name}</a>
            <form class="product-remove-form" action="${removeProductLink}" method="post" data-product-element-id="${productInfo.slug}" data-hr-id="${productInfo.slug}Hr">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                <input type="hidden" name="product_slug" value="${productInfo.slug}">
                <button type="submit" class="btn btn-danger btn-sm me-1 mt-2" title="Удалить продукт из корзины">
                    <i class="fas fa-trash"></i>
                </button>
            </form>
        </div>
        <div class="col-lg-5 col-md-6 mb-4 mb-lg-0">
            <div class="d-flex mb-4 mx-l-auto mx-auto" style="max-width: 300px">
                <form class="product-decrease-form" action="${decreaseProductLink}" method="post" data-subtotal-id="${productInfo.slug}Subtotal" data-product-quantity-input-id="${productInfo.slug}QuantityInput">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                    <input type="hidden" name="product_slug" value="${productInfo.slug}">
                    <button type="submit" class="btn btn-dark-green px-3 me-2" title="Уменьшить количество продукта в корзине">
                        <i class="fas fa-minus"></i>
                    </button>
                </form>
                <div class="form-outline text-center">
                    <input data-id="${productInfo.slug}QuantityInput" min="1" name="quantity" value="1" type="number" class="form-control" disabled="">
                    <label class="form-label m-0" for="${productInfo.slug}QuantityInput">
                        Количество
                    </label>
                </div>
                <form class="product-increase-form" action="${increaseProductLink}" method="post" data-subtotal-id="${productInfo.slug}Subtotal" data-product-quantity-input-id="${productInfo.slug}QuantityInput">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                    <input type="hidden" name="product_slug" value="${productInfo.slug}" title="Уменьшить количество продукта в корзине">
                    <button type="submit" class="btn btn-dark-green px-3 ms-2">
                        <i class="fas fa-plus"></i>
                    </button>
                </form>
            </div>
            <p class="text-center text-md-center">
                <strong data-id="${productInfo.slug}Subtotal">
                    ${subtotal}
                </strong>
                $
            </p>
        </div>
    </div>
`;
        productsListContainer.insertAdjacentHTML('beforeend', newProductElement);
        initializeCartListeners();
        initializeRemoveForms();
    });
});