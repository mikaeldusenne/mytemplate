import { Component, Vue } from "vue-property-decorator";

@Component
export default class MathMixin extends Vue {
  prettyN(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  sum(l) {
    return !l || !l.length ? 0 : l.reduce((a, b) => a + b);
  }

  mean(l) {
    if (!l || l.length == 0) {
      return NaN;
    } else {
      return this.sum(l) / l.length;
    }
  }

  variance(l) {
    if (!l || l.length == 0) {
      return NaN;
    } else {
      return this.mean(l.map(e => e * e)) - this.mean(l) ** 2;
    }
  }

  sd(l) {
    return Math.sqrt(this.variance(l));
  }

  decimalPrecision(k, n) {
    return k == 0
      ? k
      : k.toFixed(Math.max(0, -Math.floor(Math.log10(k)) + (n - 1)));
  }

}
