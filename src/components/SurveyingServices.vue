<template>
  <section class="surveying-services" id="surveying">
    <h2 class="section-title animate-on-scroll">خدمات نقشه‌برداری</h2>
    <div class="services-grid">
      <div class="service-card animate-on-scroll">
        <h3>اسکن لیزری</h3>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 250'%3E%3Crect fill='%238b6f47' width='300' height='250'/%3E%3C/svg%3E" alt="اسکن لیزری">
        <p>اسکن لیزری سه‌بعدی روشی سریع و کارآمد برای جمع‌آوری داده‌های فضایی است. جئوبیرو یکی از رهبران صنعت اسکن لیزری در بوسنی و هرزگوین است.</p>
      </div>

      <div class="service-card animate-on-scroll">
        <h3>ژئودزی مهندسی</h3>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 250'%3E%3Crect fill='%234a7c7e' width='300' height='250'/%3E%3C/svg%3E" alt="ژئودزی مهندسی">
        <p>پشتیبانی ژئودتیکی اهمیت بسیاری در طراحی و اجرای کارهای ساختمانی دارد. متخصصان نقشه‌برداری مبانی طراحی را فراهم می‌کنند و کنترل اجرای ساختارهای پیش‌بینی‌شده را انجام می‌دهند.</p>
      </div>

      <div class="service-card animate-on-scroll">
        <h3>نظارت</h3>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 250'%3E%3Crect fill='%234a9d6f' width='300' height='250'/%3E%3C/svg%3E" alt="نظارت">
        <p>تأثیرات مختلفی بر تاسیسات ساخته‌شده باعث جابه‌جایی‌های نسبی آنها در فضا می‌شود. نظارت ژئودتیکی نظام‌مند ضروری است تا این جابه‌جایی‌ها شناسایی و ثبت شوند.</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SurveyingServices'
}
</script>

<style scoped>
.surveying-services {
  padding: 20px 20px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.surveying-services > .services-grid {
  max-width: 1200px;
  width: 100%;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 70px;
  width: 100%;
  margin-top: 50px;
}

.service-card {
  background: #ffffff;
  text-align: right;
  cursor: pointer;
}

.service-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  margin-bottom: 20px;
}

.service-card h3 {
  font-size: 19px;
  font-weight: bold;
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  text-align: right;
  padding: 15px 0;
}

.service-card p {
  font-size: 14px;
  line-height: 1.8;
  color: #2a2929;
  margin-bottom: 25px;
}

@media (max-width: 1024px) {
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .surveying-services {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .surveying-services {
    padding: 30px 20px;
  }

  .service-card {
    padding: 20px;
  }

  .service-card img {
    height: 200px;
    margin-bottom: 15px;
  }

  .service-card h3 {
    font-size: 16px;
    margin-bottom: 10px;
    padding: 12px 0;
  }

  .service-card p {
    font-size: 12px;
    margin-bottom: 15px;
    line-height: 1.6;
  }
}

@media (max-width: 480px) {
  .surveying-services {
    padding: 20px 15px;
  }

  .services-grid {
    gap: 15px;
    margin-top: 20px;
  }

  .service-card {
    padding: 15px;
  }

  .service-card img {
    height: 180px;
    margin-bottom: 15px;
  }

  .service-card h3 {
    font-size: 13px;
    margin-bottom: 8px;
    padding: 10px 0;
  }

  .service-card p {
    font-size: 11px;
    margin-bottom: 12px;
    line-height: 1.6;
  }
}
</style>
