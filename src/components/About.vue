<template>
  <section class="about" id="about">
    <div class="about-content">
      <h2 class="animate-on-scroll">درباره ما</h2>
      
      <p class="animate-on-scroll">ایده جئوبیرو، که دفتر مرکزی آن در کونیک است، از سال ۱۹۹۱ وجود دارد و فعال است. فعالیت اصلی شرکت شامل تمام فعالیت‌ها در زمینه خدمات ژئودتیکی است.</p>
      <p class="animate-on-scroll">علاوه بر شرایطی که برای نیازهای گواهینامه خدمات ژئودتیکی انجام‌شده توسط کارآفرینان ژئودتیکی مستقل برآورده کرده‌ایم، ما ابزارها و تجهیزات فنی مناسبی برای انجام کار ژئودتیکی داریم.</p>
      <p class="animate-on-scroll">برای تمام تجهیزات فوق‌الذکر گواهی‌نامه‌های معتبر توسط نهادهای صالح صادر شده‌است.</p>
      
      <div class="about-features">
        <div class="feature animate-on-scroll">
          <div class="feature-icon">📋</div>
          <div>
            <h4>رویکرد حرفه‌ای</h4>
            <p>تمایل ما برای کیفیت برتر، سال‌ها تجربه و نظارت مستمر بر نیازهای بازار</p>
          </div>
        </div>
        <div class="feature animate-on-scroll">
          <div class="feature-icon">👥</div>
          <div>
            <h4>تیم متخصص</h4>
            <p>شرکت ما بیش از ۹۰ متخصص مجرب ژئودتیکی، ساختمانی و معماری را استخدام کرده است</p>
          </div>
        </div>
      </div>
    </div>
    <div class="about-image animate-on-scroll">
      <img src="/about.jpg" alt="درباره">
    </div>
  </section>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about {
  padding: 0;
  display: grid;
  grid-template-columns: 50% 50%;
  gap: 0;
  align-items: center;
  min-height: 900px;
  direction: rtl;
}

.about-image {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.about-image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.about-content {
  width: 100%;
  padding: 60px 50px;
  height: 100%;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.about-content h2 {
  font-size: 32px;
  font-weight: bold;
  padding-bottom: 16px;
  position: relative;
  margin-bottom: 20px;
}

.about-content h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 2px;
  background: #29deeb;
  transition: width 0.6s ease-out;
}

.about-content h2:hover::after {
  width: 100%;
}

.about-content p {
  padding-top: 16px;
  font-size: 14px;
  line-height: 1.8;
  margin-bottom: 20px;
  color: #2a2929;
}

.about-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-top: 40px;
}

.feature {
  display: flex;
  gap: 15px;
  padding: 15px;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature:hover {
  background: rgba(26, 188, 156, 0.1);
  transform: translateX(-8px);
}

.feature-icon {
  font-size: 24px;
  color: #00eeff;
  min-width: 30px;
}

.feature h4 {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

.feature p {
  font-size: 12px;
  color: #2a2929;
}

@media (max-width: 1024px) {
  .about {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .about-content {
    padding: 40px 30px;
    order: 2;
  }

  .about-image {
    order: 1;
    min-height: 400px;
  }
}

@media (max-width: 768px) {
  .about {
    gap: 0;
  }

  .about-content {
    padding: 30px 20px;
  }

  .about-content h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  .about-features {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 20px;
  }

  .feature {
    padding: 12px;
    min-height: 44px;
  }

  .feature-icon {
    font-size: 20px;
  }

  .feature h4 {
    font-size: 13px;
  }

  .feature p {
    font-size: 11px;
  }

  .about-image {
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .about-content {
    padding: 20px 15px;
  }

  .about-content h2 {
    font-size: 20px;
    margin-bottom: 15px;
  }

  .about-content p {
    font-size: 12px;
  }

  .about-features {
    gap: 15px;
    margin-top: 15px;
  }

  .feature {
    padding: 10px;
    min-height: 44px;
  }

  .feature-icon {
    font-size: 18px;
  }

  .feature h4 {
    font-size: 12px;
  }

  .feature p {
    font-size: 10px;
  }

  .about-image {
    min-height: 250px;
  }
}
</style>
