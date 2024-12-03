function makeMargherita() {
    return "这是一个玛格丽特披萨";
  }
  
  let pizza1 = makeMargherita();
  console.log(pizza1); // 输出：这是一个玛格丽特披萨


  function createPizza(type, size) {
    return {
      type: type,
      size: size,
      describe: function() {
        console.log("这是一个" + this.size + "寸的" + this.type + "披萨");
      }
    };
  }
  
  let pizza2 = createPizza("夏威夷", 9);
  let pizza3 = createPizza("素食", 12);
  
  pizza2.describe(); // 输出：这是一个9寸的夏威夷披萨
  pizza3.describe(); // 输出：这是一个12寸的素食披萨