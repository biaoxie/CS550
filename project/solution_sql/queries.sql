--[OK] Query 1

create view shippedVSCustDemand as
	select customerDemand.customer as customer, customerDemand.item as item, 
			decode(sum(shipOrders.qty), NULL, 0, SUM(shipOrders.qty)) as suppliedQty, 
			customerDemand.qty as demandQty
	from customerDemand left join shipOrders
		on customerDemand.customer = shipOrders.recipient
		and customerDemand.item = shipOrders.item
	group by customerDemand.customer, customerDemand.item, customerDemand.qty
	order by customer, item;

--[OK] Query 2

create view totalManufItems as 
	select manufOrders.item as item,
			decode(sum(manufOrders.qty), NULL, 0, sum(manufOrders.qty)) as totalManufQty
		from manufOrders
		group by manufOrders.item
		order by item;


-- [OK] Query 3
create view matsUsedVsShipped as
	select t1.manuf, t1.matitem, t1.requiredQty, nvl(t2.shippedQty,0) shippedQty from (
		select mo.manuf, bm.matitem, 
			sum(nvl(bm.qtymatperitem,0)* nvl(mo.qty, 0)) as requiredQty
		from manuforders mo, billofmaterials bm 
		where mo.item = bm.prodItem
		
		group by mo.manuf, bm.matitem
		order by mo.manuf, bm.matitem
	) t1
	left join 
	(
		select recipient, item, sum(qty) as shippedQty
		from shiporders
		group by recipient, item
	) t2
	on t1.manuf = t2.recipient
	and t1.matitem = t2.item
	order by t1.manuf, t1.matitem;





-- [OK] Query 4
create view producedVsShipped as
	select	manufOrders.item as item, 
			manufOrders.manuf as manuf, 
			decode(sum(shipOrders.qty), NULL, 0, SUM(shipOrders.qty)) as shippedOutQty, 
			decode(sum(manufOrders.qty), NULL, 0, SUM(manufOrders.qty)) as  orderedQty
	from manufOrders left outer join shipOrders
		on manufOrders.manuf = shipOrders.sender
		and manufOrders.item = shipOrders.item
	group by manufOrders.item, manufOrders.manuf
	order by item, manuf;


-- [OK] Query 5
create view suppliedVsShipped as
	select	supplyOrders.item as item, 
			supplyOrders.supplier as supplier, 
			supplyOrders.qty as suppliedQty, 
			decode(sum(shipOrders.qty), NULL, 0, SUM(shipOrders.qty)) as shippedQty
	from supplyOrders left join shipOrders
		on supplyOrders.supplier = shipOrders.sender
		and supplyOrders.item = shipOrders.item
	group by supplyOrders.item, supplyOrders.supplier, supplyOrders.qty
	order by item, supplier;


-- Query 6
create view perSupplierCost as
	select 	BeforeDiscount.supplier as supplier, 
			(sd.amt1 + (sd.amt2-sd.amt1)*(1-sd.disc1)+(BeforeDiscount.total-sd.amt2)*(1-sd.disc2))as cost
	from (select supplierDiscounts.supplier as supplier, 
				 sum(supplyUnitPricing.ppu * supplyOrders.qty) as total
			from supplierDiscounts left join supplyOrders
				on supplierDiscounts.supplier = supplyOrders.supplier
				left join supplyUnitPricing
					on supplyUnitPricing.supplier = supplyOrders.supplier
					and supplyUnitPricing.item = supplyOrders.item
			group by supplierDiscounts.supplier
			order by supplier) BeforeDiscount, supplierDiscounts SD
	where BeforeDiscount.supplier = SD.supplier;


-- Query 7 SKIP
create view perManufCost as
	select 	BeforeDiscount.manuf as manuf, 
			(md.amt1 + (1-md.disc1) * (BeforeDiscount.total-md.amt1)) as cost
	from (select manufDiscounts.manuf as manuf, 
			(sum(manufUnitPricing.prodCostPerUnit * manufOrders.qty + manufUnitPricing.setUpCost) ) as total
			from manufDiscounts left join manufOrders
				on manufDiscounts.manuf = manufOrders.manuf
				left join manufUnitPricing
					on manufUnitPricing.manuf = manufOrders.manuf
					and manufUnitPricing.prodItem = manufOrders.item
			group by manufDiscounts.manuf) BeforeDiscount, manufDiscounts MD 
	where BeforeDiscount.manuf = MD.manuf
	order by manuf;


-- Query 8  SKIP
create view perShipperCost as
	select sp.shipper as shipper, 
			sum (greatest(sp.minPackagePrice, 
				(sp.pricePerLb * (so.qty * it.unitWeight)))) as cost
	from shippingPricing sp, shipOrders so , items it
	where sp.shipper = so.shipper
	and so.item = it.item
    group by sp.shipper;

-- Query 9  SKIP
create view totalCostBreakDown as
	select sup.ppu as supplyCost, mp.prodCostPerUnit as manufCost, shp.minPackagePrice as shippingCost, shp.minPackagePrice as totalCost
	from supplyUnitPricing sup, manufUnitPricing mp, shippingPricing shp
		;


--[OK] Query 10
create view customersWithUnsatisfiedDemand as
	select distinct customer as customer
	from customerDemand cd 
	where 
	(
		cd.qty > (
			select sum(nvl(so.qty, 0)) from shipOrders so
			where cd.customer = so.recipient
			and cd.item = so.item
	)
	or 
		not exists (select 1 from shipOrders so
					where cd.customer = so.recipient
					and cd.item = so.item)

	)
	order by cd.customer;



--[OK] Query 11
create view suppliersWithUnsentOrders as
	select distinct sup as supplier from (
    select s.supplier as sup, s.item, s.qty unsent, nvl(a.qty, 0) as sent
        from supplyOrders s
        left join 
        (
            select sender, item, sum(sh.qty) qty
            from shipOrders sh
            group by sender, item
        ) a
        on s.supplier = a.sender and s.item = a.item
    ) 
	where  unsent > sent
	order by sup;
    

--[OK] Query 12
create view manufsWoutEnoughMats as
	select distinct manuf as manuf from (
    select s.manuf as manuf, s.matitem, s.qty unsent, nvl(a.qty, 0) as sent
        from 
        (
        select mo.manuf, bm.matitem, sum(mo.qty*bm.qtymatperitem) as qty
        from manufOrders mo, billOfMaterials bm
        where mo.item = bm.proditem
        group by mo.manuf, bm.matitem
        
        ) s
        left join 
        (
            select recipient, item, sum(sh.qty) qty
            from shipOrders sh
            group by recipient, item
            order by recipient
        ) a
        on s.manuf = a.recipient and s.matitem = a.item
    ) 
where  unsent > sent
order by manuf;
    
    
    

--[OK] Query 13
create view manufsWithUnsentOrders as
	select distinct manuf as manuf from (
    select s.manuf as manuf, s.item, s.qty unsent, nvl(a.qty, 0) as sent
        from manufOrders s
        left join 
        (
            select sender, item, sum(sh.qty) qty
            from shipOrders sh
            group by sender, item
        ) a
        on s.manuf = a.sender and s.item = a.item
    ) 
	where  unsent > sent
	order by manuf;
    
    
