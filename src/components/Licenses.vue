<template>
  <section class="licenses">
    <h2 class="section-title animate-on-scroll">مجوزها</h2>
    <div class="license-grid">
      <div class="license-item animate-on-scroll">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'%3E%3Crect fill='%23f5f5f5' width='200' height='300'/%3E%3C/svg%3E" alt="License 1">
        <p>مجوز انجام کارهای ژئودتیکی توسط کارآفرینان ژئودتیکی مستقل</p>
      </div>
      <div class="license-item animate-on-scroll">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'%3E%3Crect fill='%23f5f5f5' width='200' height='300'/%3E%3C/svg%3E" alt="License 2">
        <p>مجوز نقشه‌برداری و کارهای ژئودتیکی پایه</p>
      </div>
      <div class="license-item animate-on-scroll">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'%3E%3Crect fill='%23f5f5f5' width='200' height='300'/%3E%3C/svg%3E" alt="License 3">
        <p>مجوز انجام اندازه‌گیری‌های ژئودتیکی و معدنی در تونل‌زنی</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Licenses'
}
</script>

<style scoped>
.licenses {
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.licenses > .license-grid {
  max-width: 1200px;
  width: 100%;
}

.license-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-top: 50px;
  width: 100%;
}

.license-item {
  background: #ffffff;
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.license-item:hover {
  transform: translateY(-8px);
}

.license-item img {
  width: 100%;
  height: 350px;
  object-fit: contain;
  margin-bottom: 20px;
  transition: transform 0.3s ease-out;
}

.license-item:hover img {
  transform: scale(1.05);
}

.license-item p {
  font-size: 14px;
  color: #2a2929;
}

@media (max-width: 1024px) {
  .license-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .licenses {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .license-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .licenses {
    padding: 30px 20px;
  }

  .license-item {
    padding: 15px;
  }

  .license-item img {
    height: 250px;
  }

  .license-item p {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .licenses {
    padding: 20px 15px;
  }

  .license-grid {
    gap: 15px;
    margin-top: 20px;
  }

  .license-item {
    padding: 12px;
  }

  .license-item img {
    height: 200px;
    margin-bottom: 12px;
  }
}
</style>
