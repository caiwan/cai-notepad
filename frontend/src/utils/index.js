import moment from 'moment';

export function isPropTrue (v) {
  // Legacy stuff of category editor
  return v || v === '';
}

export function formatFuzzyDate (date) {
  return moment(new Date(date * 1000)).calendar(null, {
    sameDay: '[Today]',
    sameElse (now) {
      return `[${this.fromNow()}], YYYY-MM-DD`;
    }
  });
}
