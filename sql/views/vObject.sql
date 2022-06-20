create view vObject(
 Seed
,Depth
,Quantity
,Category
,Kind
,Enchantment
,Runic
,VaultNumber
,OpensVaultNumber
,CarriedByMonsterName
,AllyStatusName
,MutationName
) as
select
 obj.Seed
,obj.Depth
,obj.Quantity
,cat.Value
,knd.Value
,obj.Enchantment
,run.Value
,obj.VaultNumber
,obj.OpensVaultNumber
,mon.Value
,aly.Value
,mut.Value
from Object as obj
left join Category cat
  on obj.CategoryID = cat.CategoryID
left join Runic run
  on obj.RunicID = run.RunicID
left join Kind knd
  on obj.KindID = knd.KindID
left join Monster mon
  on obj.CarriedByMonsterID = mon.MonsterID
left join AllyStatus aly
  on aly.AllyStatusID = obj.AllyStatusID
left join Mutation mut
  on mut.MutationID = obj.MutationID
