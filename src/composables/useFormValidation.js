export const useFormValidation = () => {
  const errors = {};

  // Email validation
  const isValidEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  // Password validation (minimum 8 characters, at least one uppercase, one lowercase, one number)
  const isValidPassword = (password) => {
    if (password.length < 8) return false;
    return /[A-Z]/.test(password) && /[a-z]/.test(password) && /[0-9]/.test(password);
  };

  // Username validation (alphanumeric and underscore only, 3-20 characters)
  const isValidUsername = (username) => {
    const regex = /^[a-zA-Z0-9_]{3,20}$/;
    return regex.test(username);
  };

  // URL validation
  const isValidUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  // Phone number validation (basic)
  const isValidPhone = (phone) => {
    const regex = /^[\d\s\-\+\(\)]{10,}$/;
    return regex.test(phone.replace(/\s/g, ''));
  };

  // Text field validation
  const validateRequired = (value, fieldName) => {
    if (!value || value.trim() === '') {
      return `${fieldName} الزامی است`;
    }
    return null;
  };

  const validateMinLength = (value, fieldName, minLength) => {
    if (value.length < minLength) {
      return `${fieldName} باید حداقل ${minLength} کاراکتر داشته باشد`;
    }
    return null;
  };

  const validateMaxLength = (value, fieldName, maxLength) => {
    if (value.length > maxLength) {
      return `${fieldName} نمی‌تواند بیشتر از ${maxLength} کاراکتر داشته باشد`;
    }
    return null;
  };

  const validateEmail = (email) => {
    const required = validateRequired(email, 'ایمیل');
    if (required) return required;
    if (!isValidEmail(email)) {
      return 'ایمیل نامعتبر است';
    }
    return null;
  };

  const validatePassword = (password) => {
    const required = validateRequired(password, 'رمز عبور');
    if (required) return required;
    if (!isValidPassword(password)) {
      return 'رمز عبور باید حداقل 8 کاراکتر و شامل حروف بزرگ، کوچک و اعداد باشد';
    }
    return null;
  };

  const validateUsername = (username) => {
    const required = validateRequired(username, 'نام کاربری');
    if (required) return required;
    if (!isValidUsername(username)) {
      return 'نام کاربری نامعتبر است (3-20 کاراکتر، فقط حروف، اعداد و _)';
    }
    return null;
  };

  const validateUrl = (url, fieldName = 'URL') => {
    if (!url) return null; // Optional field
    if (!isValidUrl(url)) {
      return `${fieldName} نامعتبر است`;
    }
    return null;
  };

  const validateField = (value, fieldName, rules = {}) => {
    if (rules.required && !value) {
      return `${fieldName} الزامی است`;
    }

    if (rules.minLength && value.length < rules.minLength) {
      return `${fieldName} باید حداقل ${rules.minLength} کاراکتر داشته باشد`;
    }

    if (rules.maxLength && value.length > rules.maxLength) {
      return `${fieldName} نمی‌تواند بیشتر از ${rules.maxLength} کاراکتر داشته باشد`;
    }

    if (rules.email && !isValidEmail(value)) {
      return `${fieldName} نامعتبر است`;
    }

    if (rules.url && !isValidUrl(value)) {
      return `${fieldName} نامعتبر است`;
    }

    if (rules.pattern && !rules.pattern.test(value)) {
      return rules.patternMessage || `${fieldName} نامعتبر است`;
    }

    return null;
  };

  return {
    isValidEmail,
    isValidPassword,
    isValidUsername,
    isValidUrl,
    isValidPhone,
    validateRequired,
    validateMinLength,
    validateMaxLength,
    validateEmail,
    validatePassword,
    validateUsername,
    validateUrl,
    validateField
  };
};
