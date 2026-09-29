class Product:
    """
    คลาสสำหรับเก็บข้อมูลและพฤติกรรมของสินค้าแต่ละรายการ
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def update_stock(self, amount: int) -> bool:
        """ปรับปรุงจำนวนสินค้าคงเหลือ (บวกเพิ่มเมื่อรับเข้า / ลบเมื่อขาย)"""
        if self.stock + amount < 0:
            return False  # สต็อกไม่พอ
        self.stock += amount
        return True

    def calculate_total(self, quantity: int) -> float:
        """คำนวณราคารวมตามจำนวนที่ระบุ"""
        return self.price * quantity

    def is_low_stock(self, threshold: int = 5) -> bool:
        """ตรวจสอบว่าสินค้าใกล้หมดคลังหรือไม่"""
        return self.stock <= threshold

    def __str__(self):
        return f"[{self.product_id}] {self.name} | ราคา: {self.price:,.2f} บาท | คงเหลือ: {self.stock} ชิ้น"


class InventoryManager:
    """
    คลาสสำหรับควบคุมและบริหารจัดการคลังสินค้าทั้งหมด
    """
    def __init__(self):
        self.products = []

    def add_product(self, product_id: str, name: str, price: float, stock: int) -> bool:
        """เพิ่มสินค้าใหม่เข้าคลัง (ตรวจสอบ ID ซ้ำ)"""
        if self.search_product(product_id) is not None:
            print(f"❌ ข้อผิดพลาด: รหัสสินค้า {product_id} มีอยู่ในระบบแล้ว")
            return False
        
        new_product = Product(product_id, name, price, stock)
        self.products.append(new_product)
        print(f"✅ บันทึกสินค้าสำเร็จ: {name}")
        return True

    def search_product(self, product_id: str) -> Product:
        """ค้นหาสินค้าด้วย product_id"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def show_all(self):
        """แสดงรายการสินค้าทั้งหมดในคลัง"""
        print("\n=== รายการสินค้าทั้งหมดในคลัง ===")
        if not self.products:
            print("ไม่มีสินค้าในคลัง")
            return
        for product in self.products:
            print(product)
        print("===============================\n")

    def stock_in(self, product_id: str, amount: int) -> bool:
        """รับสินค้าเข้าคลัง"""
        product = self.search_product(product_id)
        if product is None:
            print(f"❌ ข้อผิดพลาด: ไม่พบรหัสสินค้า {product_id}")
            return False
        
        if amount <= 0:
            print("❌ ข้อผิดพลาด: จำนวนต้องมากกว่า 0")
            return False

        product.update_stock(amount)
        print(f"📥 รับสินค้าเข้าสำเร็จ: {product.name} เพิ่ม {amount} ชิ้น (คงเหลือ: {product.stock} ชิ้น)")
        return True

    def stock_out(self, product_id: str, amount: int) -> bool:
        """ขายสินค้า / ตัดสต็อก"""
        product = self.search_product(product_id)
        if product is None:
            print(f"❌ ข้อผิดพลาด: ไม่พบรหัสสินค้า {product_id}")
            return False

        if amount <= 0:
            print("❌ ข้อผิดพลาด: จำนวนต้องมากกว่า 0")
            return False

        if product.stock < amount:
            print(f"❌ ข้อผิดพลาด: สินค้าในคลังไม่เพียงพอ (ต้องการ {amount} ชิ้น, มีเหลือ {product.stock} ชิ้น)")
            return False

        product.update_stock(-amount)
        total_price = product.calculate_total(amount)
        print(f"🛒 ขายสำเร็จ! สินค้า: {product.name} จำนวน {amount} ชิ้น | ราคารวม: {total_price:,.2f} บาท (คงเหลือ: {product.stock} ชิ้น)")
        return True

    def check_low_stock(self, threshold: int = 5):
        """ตรวจสอบและแจ้งเตือนรายการสินค้าที่ใกล้หมดคลัง"""
        print(f"\n⚠️ === รายงานสินค้าเตือนภัย (คงเหลือ <= {threshold} ชิ้น) ===")
        low_stock_list = [p for p in self.products if p.is_low_stock(threshold)]
        
        if not low_stock_list:
            print("ไม่มีสินค้าที่อยู่ในเกณฑ์ใกล้หมด")
        else:
            for p in low_stock_list:
                print(f"- [{p.product_id}] {p.name} คงเหลือ: {p.stock} ชิ้น")
        print("====================================================\n")


# ==========================================
# ส่วนสำหรับทดสอบตาม Test Cases ในเอกสารข้อเสนอ
# ==========================================
if __name__ == "__main__":
    print("--- เริ่มต้นการทดสอบระบบคลังสินค้า (Core Test Cases) ---")
    
    inv = InventoryManager()

    # เพิ่มข้อมูลเริ่มต้น
    inv.add_product("P01", "ปากกาน้ำเงิน", 15.0, 10)
    inv.add_product("P02", "สมุดโน้ต A5", 45.0, 3)

    inv.show_all()

    # Test Case 1: ขายสินค้า (สต็อกพอ) - ID: P01, ขาย 2 ชิ้น (จากเดิม 10)
    print("\n--- Test Case 1: ขายสินค้า (สต็อกพอ) ---")
    inv.stock_out("P01", 2)

    # Test Case 2: ขายสินค้า (สต็อกไม่พอ) - ID: P01, ขาย 15 ชิ้น (คงเหลือจริง 8)
    print("\n--- Test Case 2: ขายสินค้า (สต็อกไม่พอ) ---")
    inv.stock_out("P01", 15)

    # Test Case 3: ค้นหาสินค้าที่ไม่มี - ID: P99
    print("\n--- Test Case 3: ค้นหาสินค้าที่ไม่มี ---")
    inv.stock_out("P99", 1)

    # Test Case 4: เช็คสินค้าใกล้หมด (Threshold <= 5)
    print("\n--- Test Case 4: เช็คสินค้าใกล้หมด ---")
    inv.check_low_stock(threshold=5)