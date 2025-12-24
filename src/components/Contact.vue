<template>
  <section class="contact" id="contact">
    <h2 class="section-title animate-on-scroll">تماس با ما</h2>
    <div class="contact-container">
      <div class="contact-form animate-on-scroll">
        <div class="form-group">
          <input type="text" placeholder="نام شما">
        </div>
        <div class="form-group">
          <input type="tel" placeholder="شماره تلفن شما">
        </div>
        <div class="form-group">
          <input type="email" placeholder="ایمیل شما">
        </div>
        <div class="form-group">
          <textarea placeholder="پیام شما"></textarea>
        </div>
        <div class="success-message">
          <div class="success-check">✓</div>
          <span>ارسال شد!</span>
        </div>
        <button class="btn-send">ارسال</button>
      </div>
      <div class="contact-map animate-on-scroll">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'%3E%3Crect fill='%2366bb6a' width='400' height='400'/%3E%3C/svg%3E" alt="نقشه">
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Contact'
}
</script>

<style scoped>
.contact {
  padding: 60px 50px;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.contact > .contact-container {
  max-width: 1200px;
  width: 100%;
}

.contact-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  margin-top: 50px;
  width: 100%;
}

.contact-map {
  border-radius: 8px;
  overflow: hidden;
}

.contact-map img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.contact-map:hover img {
  transform: scale(1.05);
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group input,
.form-group textarea {
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  min-height: 50px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #1abc9c;
}

.form-group textarea {
  min-height: 120px;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #999;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.success-check {
  width: 30px;
  height: 30px;
  background: #27ae60;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.btn-send {
  background: #1abc9c;
  color: white;
  padding: 15px 40px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  min-height: 44px;
}

.btn-send:hover {
  background: #16a085;
  transform: translateY(-2px);
}

.btn-send:active {
  transform: translateY(0);
}

@media (max-width: 1024px) {
  .contact {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .contact {
    padding: 30px 20px;
  }

  .contact-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .contact-map img {
    height: 300px;
  }

  .form-group input,
  .form-group textarea {
    padding: 12px;
    font-size: 13px;
    min-height: 44px;
  }

  .btn-send {
    padding: 12px 30px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .contact {
    padding: 20px 15px;
  }

  .contact-map img {
    height: 250px;
  }

  .form-group input,
  .form-group textarea {
    padding: 10px;
    font-size: 12px;
    min-height: 44px;
  }

  .form-group textarea {
    min-height: 100px;
  }

  .btn-send {
    padding: 10px 25px;
    font-size: 11px;
    min-height: 44px;
  }
}
</style>
