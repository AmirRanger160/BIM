<template>
  <section class="certificates">
    <h2 class="section-title animate-on-scroll">گواهی‌نامه‌ها</h2>
    <div class="cert-grid">
      <div class="cert-item animate-on-scroll">
        <img src="../../public/ISO14001.jpg.webp" alt="Certificate 1">
        <p>ISO 9001:2015, ISO 14001:2015 و ISO 45001:2018</p>
      </div>
      <div class="cert-item animate-on-scroll">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'%3E%3Crect fill='%23f5f5f5' width='200' height='300'/%3E%3C/svg%3E" alt="Certificate 2">
        <p>ISO/IEC 27001:2017</p>
      </div>
      <div class="cert-item animate-on-scroll">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 300'%3E%3Crect fill='%23f5f5f5' width='200' height='300'/%3E%3C/svg%3E" alt="Certificate 3">
        <p>گواهینامه پلاتینی تعالی اعتباری</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Certificates'
}
</script>

<style scoped>
.certificates {
  padding: 60px 50px;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.certificates > .cert-grid {
  max-width: 1200px;
  width: 100%;
}

.cert-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-top: 50px;
  width: 100%;
}

.cert-item {
  background: #f9f9f9;
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cert-item:hover {
  transform: translateY(-8px);
}

.cert-item img {
  width: 100%;
  height: 350px;
  object-fit: contain;
  margin-bottom: 20px;
  transition: transform 0.3s ease-out;
}

.cert-item:hover img {
  transform: scale(1.05);
}

.cert-item p {
  font-size: 14px;
  color: #2a2929;
}

@media (max-width: 1024px) {
  .cert-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .certificates {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .cert-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .certificates {
    padding: 30px 20px;
  }

  .cert-item {
    padding: 15px;
  }

  .cert-item img {
    height: 250px;
  }

  .cert-item p {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .certificates {
    padding: 20px 15px;
  }

  .cert-grid {
    gap: 15px;
    margin-top: 20px;
  }

  .cert-item {
    padding: 12px;
  }

  .cert-item img {
    height: 200px;
    margin-bottom: 12px;
  }
}
</style>
