<template>
  <footer>
    <div class="footer-contact">
      <h3>تماس</h3>
      <p>دفتر مرکزی : زعفرانیه، تقاطع بلوار بهزادی و ماکویی پور، ساختمان سروین، طبقه 3، واحد 33</p>
      <p>تلفن: <a href="tel:+38761542490">+387 61 542 490</a></p>
      <p>ایمیل: <a href="mailto:info@geobiro.ba">info@geobiro.ba</a></p>
      
      <div class="footer-logos">
        <img src="/cert.png" alt="Certificate">
      </div>
    </div>
    <div>
      <h3>ناوبری</h3>
      <a href="#home">صفحه اول</a>
      <a href="#bim">خدمات BIM</a>
      <a href="#surveying">خدمات نقشه‌برداری</a>
      <a href="#about">درباره</a>
      <a href="#contact">تماس</a>
    </div>
    <div>
      <div class="footer-logo">
        <a href="/">
          <img src="/logo-foter-bim.png" alt="BIM Logo" class="footer-logo-img">
        </a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; ۲۰۲۴ مشاور بیم. تمام حقوق محفوظ است.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
footer {
  background: linear-gradient(rgba(26, 26, 26, 0.85), rgba(26, 26, 26, 0.85)), url('/footer-bg.jpg') no-repeat center/cover;
  background-attachment: fixed;
  color: #999;
  padding: 80px 50px 30px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 60px;
  direction: rtl;
  min-height: 500px;
}

.footer-logo {
  margin-bottom: 30px;
  flex-basis: 100%;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-logo-img {
  max-width: 200px;
  height: auto;
  object-fit: contain;
}

footer h3 {
  color: white;
  font-size: 14px;
  text-transform: uppercase;
  margin-bottom: 20px;
  font-weight: bold;
}

footer a {
  color: #87CEEB;
  text-decoration: none;
  font-size: 14px;
  display: block;
  margin-bottom: 10px;
  transition: color 0.3s;
}

footer a:hover {
  color: white;
}

.footer-contact p {
  font-size: 14px;
  margin-bottom: 10px;
  color: #999;
}

.footer-contact a {
  display: inline;
  margin: 0;
}

.footer-logos {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.footer-logos img {
  height: 40px;
  object-fit: contain;
}

.footer-bottom {
  width: 100%;
  border-top: 1px solid #333;
  text-align: center;
  color: #636363;
  font-size: 12px;
  background-color: #121212;
  padding: 20px 0;
  margin-top: 20px;
}

@media (max-width: 1024px) {
  footer {
    padding: 40px 30px 20px;
    gap: 40px;
  }
}

@media (max-width: 768px) {
  footer {
    grid-template-columns: 1fr;
    padding: 30px 20px 20px;
    gap: 30px;
  }

  .footer-logo {
    font-size: 22px;
    margin-bottom: 15px;
  }

  footer h3 {
    font-size: 12px;
    margin-bottom: 10px;
  }

  footer a {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .footer-contact p {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .footer-logos img {
    height: 30px;
  }
}

@media (max-width: 480px) {
  footer {
    padding: 20px 15px 15px;
    gap: 20px;
  }

  .footer-logo {
    font-size: 18px;
    margin-bottom: 12px;
  }

  footer h3 {
    font-size: 11px;
    margin-bottom: 8px;
  }

  footer a {
    font-size: 11px;
    margin-bottom: 6px;
  }

  .footer-contact p {
    font-size: 11px;
    margin-bottom: 6px;
  }

  .footer-logos img {
    height: 25px;
  }
}
</style>
