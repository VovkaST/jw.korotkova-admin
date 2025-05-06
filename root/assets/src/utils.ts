export function formatPrice(value: string | number, currency: string = 'RUB') {
  return parseFloat(value).toLocaleString('ru-RU', {
    style: 'currency',
    currency: currency,
  });
}
