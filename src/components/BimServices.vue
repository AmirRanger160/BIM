<template>
  <section class="bim-services" id="bim">
    <h2 class="section-title animate-on-scroll">خدمات BIM</h2>
    <div class="services-grid">
      <div class="service-card animate-on-scroll">
        <h3>مدل‌سازی سه‌بعدی</h3>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 250'%3E%3Crect fill='%23ddd' width='300' height='250'/%3E%3C/svg%3E" alt="مدل‌سازی سه‌بعدی">
        <p>تخصص ما در ایجاد مدل‌های BIM آماده با توجه به داده‌های ابر نقطه (اسکن لیزری) در نرم‌افزارهای مختلف است. تیم اختصاصی ما برای کمک به شما در پیاده‌سازی منافع فرایند Scan to BIM در شرکت خود آماده است.</p>
        <p style="margin-top: 15px;">نرم‌افزارهای مجاز مورد استفاده:</p>
        <div class="software-logos">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="Revit">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="ArchiCAD">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="Allplan">
        </div>
      </div>

      <div class="service-card animate-on-scroll">
        <h3>بررسی ساختمان اندازه‌گیری شده</h3>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 250'%3E%3Crect fill='%23333' width='300' height='250'/%3E%3C/svg%3E" alt="بررسی ساختمان">
        <p>داشتن نقشه‌های دوبعدی کافی و به‌روز ضروری برای تمام پروژه‌های بزرگ است. از آنجایی که ابرهای نقطه تمام اطلاعات مربوط به ظاهر یک شی موجود را ارائه می‌دهند، می‌توان تمام ویژگی‌ها را براساس سطح جزئیات نشان داد.</p>
        <p style="margin-top: 15px;">نرم‌افزارهای مجاز مورد استفاده:</p>
        <div class="software-logos">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="AutoCAD">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="Software 2">
        </div>
      </div>

      <div class="service-card animate-on-scroll">
        <h3>ثبت ابر نقطه</h3>
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 250'%3E%3Crect fill='%232d5f3f' width='300' height='250'/%3E%3C/svg%3E" alt="ثبت ابر نقطه">
        <p>تیم ما از نرم‌افزارهای پیشرو در پردازش و تحلیل ابر نقطه استفاده می‌کند. اگر داده‌های اسکن لیزری خام (یا روش‌های دیگر جمع‌آوری ابر نقطه) به هر فرمتی دارید، تیم ما آماده است ابر نقطه‌ای ثبت‌شده و فهرس‌شده تحویل دهد.</p>
        <p style="margin-top: 15px;">نرم‌افزارهای مجاز مورد استفاده:</p>
        <div class="software-logos">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="Software 1">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 50'%3E%3Crect fill='%23e0e0e0' width='100' height='50'/%3E%3C/svg%3E" alt="Software 2">
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'BimServices'
}
</script>

<style scoped>
.bim-services {
  padding: 20px 20px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bim-services > .services-grid {
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

.software-logos {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
}

.software-logos img {
  height: 40px;
  object-fit: contain;
  transition: transform 0.3s ease-out;
}

.software-logos img:hover {
  transform: scale(1.1);
}

@media (max-width: 1024px) {
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .bim-services {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .bim-services {
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
  }

  .software-logos {
    gap: 10px;
  }

  .software-logos img {
    height: 30px;
  }
}

@media (max-width: 480px) {
  .bim-services {
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

  .software-logos img {
    height: 25px;
  }
}
</style>
